from django.db import models

# Create your models here.

class ChatRoom(models.Model):
    blog = models.OneToOneField('blogs.Blog', on_delete=models.CASCADE, related_name='chat_room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for '{self.blog.title}'"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey('blogs.Author', on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message by {self.user.user.username} in {self.room.blog.title} at {self.timestamp}'