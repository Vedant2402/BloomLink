from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch

# Create your models here.

class ConversationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            Prefetch('participants', queryset=User.objects.only('id', 'username'))
        )
        
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ConversationManager()

    def __str__(self):
        return f"Conversation {self.id} with participants: {[user.username for user in self.participants.all()]}"