from django.urls import path
from . import views

urlpatterns = [
    path('blog/<int:blog_id>/chat/', views.chat_room, name='blog-chat'),
    path('api/chat/<int:blog_id>/messages/', views.chat_messages_api, name='chat-messages-api'),
]