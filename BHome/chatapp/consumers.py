# sync func in python

from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer
import jwt
import JWT
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import *
from urllib.parse import parse_qs

User = get_user_model()

#interface features
#online, msg seen, typing, last seen, read receipts, delivery receipts, group chats, media sharing, voice and video calls, message reactions, end-to-end encryption, message search, message forwarding, message deletion, message editing, user presence indicators, status updates, chatbots and automation, multi-device support, cross-platform compatibility, user blocking and reporting, chat archiving and backup

class ChatConsumer(WebsocketConsumer):
    
    async def connect(self):
        query_string = self.scope['query_string'].decode('utf8')
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]
        
        if token:
            try:
                payload = JWT.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                self.user = await self.get_user(payload['user_id'])
                self.scope['user'] = self.user
                self.accept()
            except  jwt.ExpiredSignatureError:
                await self.close(code=4000)
                return
            except jwt.InvalidTokenError:
                await self.close(code=4001)
                return
        else:
            await self.close(code=4002) #close the conection if no token is provided
            return
        
        #add channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        #accept websocket connections
        
        await self.accept()
        
        user_data = await self.get_user_data(self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_status',
                'online_users': [user_data],
                status: 'online'
            })
        
    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            #notify others about the disconnect
            user_data = await self.get_user_data(self.scope["user"])
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_status',
                    'online_users': [user_data],
                    status: 'offline'
                }
            )
            
            
    # help aceept and recive messages from the WebSocket        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get('type')
        
        if event_type == 'chat_message':
            message_content = text_data_json.get('message')
            user_id = text_data_json.get('user')
            
            try:
                user = await self.get_user(user_id)
                conversation = await self.get_conversation(
                    self.get_conversation_id)
                from .serializers import UserListSerializer
                user_date = UserListSerializer(user).data
                
                message = await self.save_message(conversation, user, message_content)
                
                await sef.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message.content,
                        'user': user_data,
                        'timestamp': message.timestamp.isoformat(),
                    }
                )
            except Exception as e:
                print(f"Error saving message: {e}")
                
        elif event_type == 'typing':
            try:
                user_data = await self.get_user_data(self.scope['user'])
                recver_id = text_data_json.get('receiver_id')
                
                if receiver_id is not None:
                    if isinstance(receiver_id, (str, int, float)):
                        receiver_id = (receiver_id)
                        
                        if receiver_id != self.scope['user'].id:
                            print(f"User {
                                user_data['username']} is typing to user with id {receiver_id}"
                            )
                            await self.channel_layer.group_send(
                                self.room_group_name,
                                {
                                    'type': 'typing',
                                    'user': user_data,
                                    'receiver_id': receiver_id
                                }
                            )
                        else:
                            print(f"{user_id['username']} is typing to themselves")
                    else:
                        print(f"Invalid receiver ID: {type(receiver_id)}")
                        
                else:
                    print("No receiver ID provided for typing event")
            
            except Exception as e:
                print(f"Error parsing receiver ID: {e}")
            except Exception as e:
                print(f"Error getting user data: {e}")
                

    #chat messages helper function
    async def cha

                        