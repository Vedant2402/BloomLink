# WebSocket consumer for chat: use async consumer and fix logic/typos

import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import Conversation, Message
from urllib.parse import parse_qs

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Parse token from query string
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]

        if not token:
            await self.close(code=4002)
            return

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id') or payload.get('user')
            self.user = await self.get_user(user_id)
            if not self.user:
                await self.close(code=4003)
                return
            self.scope['user'] = self.user
        except jwt.ExpiredSignatureError:
            await self.close(code=4000)
            return
        except jwt.InvalidTokenError:
            await self.close(code=4001)
            return

        # conversation id from URL route kwargs
        self.conversation_id = self.scope['url_route']['kwargs'].get('conversation_id')
        self.room_group_name = f'conversation_{self.conversation_id}'

        # add channel to group and accept
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # notify group of online status
        user_data = await self.get_user_data(self.user)
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'online_status',
            'online_users': [user_data],
            'status': 'online',
        })

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            user_data = await self.get_user_data(self.scope.get('user'))
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'online_status',
                'online_users': [user_data],
                'status': 'offline',
            })
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return
        try:
            text_data_json = json.loads(text_data)
        except Exception:
            return

        event_type = text_data_json.get('type')

        if event_type == 'chat_message':
            message_content = text_data_json.get('message')
            user_id = text_data_json.get('user')

            try:
                user = await self.get_user(user_id)
                conversation = await self.get_conversation(self.conversation_id)
                from .serializers import UserListSerializer
                user_data = UserListSerializer(user).data

                message = await self.save_message(conversation, user, message_content)

                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'chat_message',
                    'message': message.content,
                    'user': user_data,
                    'timestamp': message.timestamp.isoformat(),
                })
            except Exception as e:
                # log and ignore errors to avoid crashing consumer
                print(f"Error saving message: {e}")

        elif event_type == 'typing':
            try:
                user_data = await self.get_user_data(self.scope.get('user'))
                receiver_id = text_data_json.get('receiver_id')
                is_typing = text_data_json.get('is_typing', True)

                await self.channel_layer.group_send(self.room_group_name, {
                    'type': 'typing',
                    'user': user_data,
                    'receiver_id': receiver_id,
                    'is_typing': is_typing,
                })
            except Exception as e:
                print(f"Error handling typing event: {e}")

    # handlers for events sent to the group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event.get('message'),
            'user': event.get('user'),
            'timestamp': event.get('timestamp'),
        }))

    async def typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': event.get('user'),
            'receiver_id': event.get('receiver_id'),
            'is_typing': event.get('is_typing'),
        }))

    async def online_status(self, event):
        await self.send(text_data=json.dumps(event))

    # helper functions to interact with the database (run in threadpool)
    @sync_to_async
    def get_user(self, user_id):
        if not user_id:
            return None
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def get_user_data(self, user):
        from .serializers import UserListSerializer
        if not user:
            return {}
        return UserListSerializer(user).data

    @sync_to_async
    def get_conversation(self, conversation_id):
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @sync_to_async
    def save_message(self, conversation, user, content):
        return Message.objects.create(conversation=conversation, sender=user, content=content)