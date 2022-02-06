from django.contrib import admin
from .models import ChatRoom, Message

#Custom Account Admin
class ChatRoomAdmin(admin.ModelAdmin):
    fields = ('name', 'key', 'users')
    search_fields = ('title',)

    list_per_page = 50

    class Meta:
        model = ChatRoom

class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'timestamp', 'content')
    list_filter = ['room',  'user', "timestamp"]
    search_fields = ('content', 'room')
    readonly_fields = ['user', 'room', 'timestamp']

    list_per_page = 100

    class Meta:
        model = Message

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)