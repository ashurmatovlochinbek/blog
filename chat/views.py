from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from blogs.models import Blog
from chat.models import Message


# Create your views here.

@login_required
def chat_room(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request, 'chat/chat_room.html', {'blog': blog})



@login_required
def chat_messages_api(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        room = blog.chat_room
    except Blog.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)

    # Get offset (how many messages to skip)
    offset = int(request.GET.get('offset', 0))
    limit = int(request.GET.get('limit', 20))

    messages_qs = Message.objects.filter(room=room).select_related('user__user')
    messages = messages_qs[offset:offset + limit]

    if not messages:
        return JsonResponse({'messages': [], 'has_more': False})

    data = [
        {
            'id': msg.id,
            'author_username': msg.user.user.username,  # ✅ Correct!
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat(),
        }
        for msg in messages
    ]

    # Check if more older messages exist
    has_more = messages_qs[offset + limit:offset + limit + 1].exists()

    return JsonResponse({
        'messages': data,
        'has_more': has_more,
        'next_offset': offset + limit,
    })