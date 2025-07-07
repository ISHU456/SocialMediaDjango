from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Type your message...',
            'id': 'message-input'
        }),
        max_length=1000
    )
    
    class Meta:
        model = Message
        fields = ['content'] 