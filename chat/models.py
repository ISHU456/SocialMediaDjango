from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = [user.username for user in self.participants.all()]
        return f"Conversation between {' and '.join(participant_names)}"
    
    def get_other_participant(self, current_user=None):
        """Get the other participant in the conversation"""
        if current_user is None:
            return self.participants.first()
        return self.participants.exclude(id=current_user.id).first()
    
    def get_last_message(self):
        """Get the last message in the conversation"""
        return self.messages.order_by('-created_at').first()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"
    
    def mark_as_read(self):
        """Mark the message as read"""
        self.is_read = True
        self.save()


class ChatNotification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chat_notifications')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Chat notification for {self.recipient.username} from {self.sender.username}"
