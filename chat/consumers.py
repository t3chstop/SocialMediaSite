import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from asgiref.sync import sync_to_async

"""
TO DO: 
-make an entrance page that asks for a room to enter. It only needs to ask for the name, 
and should pick up the user who sent it based on who is logged in. Login required for this
view.
-Create a room page that has an input section for a message(dw about images for now) and
sends this information to the backend multiple times
-Store messages in database, so that previous messages appear in the chatroom

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

    async def disconnect(self, close_code):
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
        roomName = text_data_json['room']

        await self.save_message(displayName, roomName, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'displayName' : displayName,
                'roomName' : roomName
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        displayName = event['displayName']
        roomName = event['roomName']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'displayName' : displayName,
            'roomName' : roomName
        }))

    @sync_to_async
    def save_message(self, displayName, room, message):
        Message.objects.create(displayName=displayName, room=room, content=message)