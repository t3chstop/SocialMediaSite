import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, ChatRoom
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name
		self.roomobj = sync_to_async(ChatRoom.objects.get)(name=self.room_name)

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
		print('reached')
		await self._save_message(room_=self.roomobj, content_=message, user_=self.scope['user'])
		print('here')
		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message
			}
		)

	def _save_message(room_, content_, user_):
		Message.objects.create(room=room_, message=content_, user=user_)
		print('reached2')

	# Receive message from room group
	async def chat_message(self, event):
		message = event['message']
		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'message': message
		}))