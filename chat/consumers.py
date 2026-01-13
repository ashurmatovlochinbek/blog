# from channels.generic.websocket import AsyncWebsocketConsumer
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#
#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': text_data
#             }
#         )
#
#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event['message']
#
#         # Send message to WebSocket
#         await self.send(text_data=message)


import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from blogs.models import Blog
from .models import Message  # assumes Message is in chat/models.py


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get blog_id from URL route
        self.blog_id = self.scope['url_route']['kwargs']['blog_id']

        # Fetch blog and ensure it exists
        try:
            self.blog = await self.get_blog(self.blog_id)
        except ObjectDoesNotExist:
            await self.close(code=4001)  # custom close code: invalid blog
            return

        # Ensure user is authenticated
        if not self.scope["user"].is_authenticated:
            await self.close(code=4002)  # custom: unauthenticated
            return

        # Create room group name (must be string)
        self.room_group_name = f"chat_blog_{self.blog_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (frontend → backend)
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_text = data.get("message", "").strip()
        except (json.JSONDecodeError, AttributeError):
            return  # ignore malformed data

        if not message_text:
            return

        user = self.scope["user"]

        # Save message to DB
        message_obj = await self.save_message(user, message_text)

        # Prepare message data to broadcast
        event_data = {
            "id": message_obj.id,
            "author_id": user.id,
            "author_username": user.username,  # or user.email, etc.
            "content": message_text,
            "timestamp": message_obj.timestamp.isoformat(),
        }

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": event_data,
            }
        )

    # Receive message from room group (backend → frontend)
    async def chat_message(self, event):
        # Send message to WebSocket (to one user)
        await self.send(text_data=json.dumps(event["message"]))

    # --- Helper methods (database operations) ---

    @database_sync_to_async
    def get_blog(self, blog_id):
        return Blog.objects.get(id=blog_id)

    @database_sync_to_async
    def save_message(self, user, content):
        # Get the ChatRoom (via blog)
        room = self.blog.chat_room

        # Get the Author linked to this user
        author = user.author  # ← assumes every user has an Author (you must ensure this!)

        return Message.objects.create(
            room=room,
            user=author,  # ✅ correct field name
            content=content
        )