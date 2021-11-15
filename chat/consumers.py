import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async
from accounts.models import Account

"""
TO DO: 
-Automatically generate chatrooms between friends when the friendship is created
"""



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, messagecode):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        displayName = text_data_json['displayName']
        user = self.scope['user']
        profile_picture_path = user.profile_picture.url
        roomName = text_data_json['room']

        await self.save_message(user, roomName, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'displayName' : displayName,
                'roomName' : roomName,
                'profile_picture_url' : profile_picture_path,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        displayName = event['displayName']
        user = self.scope['user']
        profile_picture_path = user.profile_picture.url
        print(profile_picture_path)
        roomName = event['roomName']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'displayName' : displayName,
            'roomName' : roomName,
            'profile_picture_url' : profile_picture_path,
        }))

    @sync_to_async
    def save_message(self, user, room, message):
        Message.objects.create(user=user, room=room, content=message)