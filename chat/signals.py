from django.db.models.signals import post_save
from django.dispatch import receiver
from chat.models import ChatRoom
from blogs.models import Blog


@receiver(post_save, sender=Blog)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        ChatRoom.objects.create(blog=instance)