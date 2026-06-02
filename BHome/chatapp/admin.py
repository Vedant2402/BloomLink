from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
	list_display = ('id', 'created_at', 'participant_count')
	search_fields = ('participants__username',)
	filter_horizontal = ('participants',)

	def participant_count(self, obj):
		return obj.participants.count()

	participant_count.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'conversation', 'sender', 'timestamp')
	search_fields = ('content', 'sender__username')
	list_filter = ('timestamp', 'sender')
