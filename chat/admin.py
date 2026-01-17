from django.contrib import admin

from chat.models import ChatRoom, Message


# Register your models here.

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_per_page = 20

