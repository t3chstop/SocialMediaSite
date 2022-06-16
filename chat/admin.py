from django.contrib import admin
from .models import ChatRoom, Message

#Custom Account Admin
class ChatRoomAdmin(admin.ModelAdmin):
    fields = ('name', 'users')
    search_fields = ('name',)

    list_per_page = 50

    class Meta:
        model = ChatRoom

class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'room', 'user', 'timestamp', )
    list_filter = ['room',  'user', "timestamp"]
    search_fields = ('content', 'room')

    list_per_page = 100

    class Meta:
        model = Message

admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)