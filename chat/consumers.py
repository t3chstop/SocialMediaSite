import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, ChatRoom
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

		#Check if user is authorized
		# thisroom = database_sync_to_async(ChatRoom.objects.get)(pk=self.room_name)
		# if not self.scope['user'] in thisroom.users:
		# 	pass
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
		await self.save_message(self.scope['user'], self.room_name, message)
		print(self.scope['user'].profile_picture.url)
		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message,
				'profile_path' : self.scope['user'].profile_picture.url
			}
		)

	@database_sync_to_async
	def save_message(self, user, roomkey, content):
		room = ChatRoom.objects.get(pk=roomkey)
		msg = Message.objects.create(user=user, room=room, content=content)
		msg.save()


	

	# Receive message from room group
	async def chat_message(self, event):
		message = event['message']
		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'type': 'chat_message',
			'message': message,
			'profile_path' : self.scope['user'].profile_picture.url
		}))