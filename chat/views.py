from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Conversation, Message, ChatNotification
from .forms import MessageForm
from profiles.models import Profile


@login_required
def chat_list(request):
    """Display list of conversations"""
    # Get all conversations where the user is a participant
    conversations = request.user.conversations.all()
    
    # Get unread message counts for each conversation and other participant
    for conversation in conversations:
        conversation.unread_count = conversation.messages.filter(
            ~Q(sender=request.user) & Q(is_read=False)
        ).count()
        conversation.other_participant = conversation.get_other_participant(request.user)
    
    context = {
        'conversations': conversations,
        'current_user': request.user,
    }
    return render(request, 'chat/chat_list.html', context)


@login_required
def chat_room(request, conversation_id):
    """Display chat room for a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    other_user = conversation.get_other_participant(request.user)
    
    # Mark messages as read
    conversation.messages.filter(~Q(sender=request.user)).update(is_read=True)
    
    # Get messages with pagination
    messages = conversation.messages.all()
    paginator = Paginator(messages, 50)  # Show last 50 messages
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    form = MessageForm()
    
    context = {
        'conversation': conversation,
        'other_user': other_user,
        'messages': page_obj,
        'form': form,
    }
    return render(request, 'chat/chat_room.html', context)


@login_required
def start_conversation(request, username):
    """Start a new conversation with a user"""
    other_user = get_object_or_404(User, username=username)
    
    if other_user == request.user:
        return redirect('chat:chat_list')
    
    # Check if conversation already exists
    existing_conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_conversation:
        return redirect('chat:chat_room', conversation_id=existing_conversation.id)
    
    # Create new conversation
    conversation = Conversation.objects.create()
    conversation.participants.add(request.user, other_user)
    
    return redirect('chat:chat_room', conversation_id=conversation.id)


@login_required
def send_message(request, conversation_id):
    """AJAX endpoint to send a message"""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        form = MessageForm(request.POST)
        
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            
            # Create notification for other participants
            other_participants = conversation.participants.exclude(id=request.user.id)
            for participant in other_participants:
                ChatNotification.objects.create(
                    recipient=participant,
                    sender=request.user,
                    conversation=conversation,
                    message=message
                )
            
            return JsonResponse({
                'success': True,
                'message_id': message.id,
                'content': message.content,
                'sender': message.sender.username,
                'created_at': message.created_at.strftime('%H:%M'),
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def get_messages(request, conversation_id):
    """AJAX endpoint to get new messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    # Get messages after a certain timestamp (for real-time updates)
    last_message_id = request.GET.get('last_message_id')
    if last_message_id and last_message_id.isdigit():
        try:
            last_message_id = int(last_message_id)
            messages = conversation.messages.filter(id__gt=last_message_id).order_by('created_at')
        except ValueError:
            messages = conversation.messages.none()
    else:
        # If no last_message_id provided, return empty list to prevent duplicate loading
        messages = conversation.messages.none()
    
    # Mark messages as read
    messages.filter(~Q(sender=request.user)).update(is_read=True)
    
    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'is_own': message.sender == request.user,
            'created_at': message.created_at.strftime('%H:%M'),
        })
    
    return JsonResponse({
        'messages': messages_data,
        'unread_count': conversation.messages.filter(~Q(sender=request.user) & Q(is_read=False)).count()
    })


@login_required
def get_unread_count(request):
    """AJAX endpoint to get unread message count"""
    total_unread = 0
    conversations_data = []
    
    for conversation in request.user.conversations.all():
        unread_count = conversation.messages.filter(~Q(sender=request.user) & Q(is_read=False)).count()
        if unread_count > 0:
            total_unread += unread_count
            other_user = conversation.get_other_participant(request.user)
            conversations_data.append({
                'conversation_id': conversation.id,
                'other_user': other_user.username,
                'unread_count': unread_count,
                'last_message': conversation.get_last_message().content if conversation.get_last_message() else ''
            })
    
    return JsonResponse({
        'total_unread': total_unread,
        'conversations': conversations_data
    })


@login_required
def search_users(request):
    """Search users to start conversations with"""
    query = request.GET.get('q', '')
    users = []
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:10]
    
    context = {
        'users': users,
        'query': query,
    }
    return render(request, 'chat/search_users.html', context)
