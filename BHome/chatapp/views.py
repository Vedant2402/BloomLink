from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.exceptions import PermissionDenied, NotFound

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# listing of users
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
#creating, listing and viewing conversations

class ConversationListCrateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return (conversation.objects.filter(participants=self.request.user).prefetch_related('participants'))
    
    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        
        if len(participants_ids) != 2:
            return Response({'error': 'At least two participants are required to create a conversation.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        if str(request.user.id) not in participants_ids:
            return Response(
                {'error': 'You must be a participant in the conversation.'}, 
                            status=status.HTTP_403_FORBIDDEN)
            
        users = User.objects.filter(id__in=participants_data)
        if users.count() != 2:
            return Response({'error': 'One or more participants not found.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
            
        existing_conversation = Conversation.objects.filter(
            participants__id=participants_data[0]
            ).filter(
                participants__id=participants_data[1]
            ).distinct()