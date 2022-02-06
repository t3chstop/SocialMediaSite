from django.shortcuts import redirect, render
from .forms import CreateChatRoomForm
from .models import ChatRoom
from django.contrib.auth.decorators import login_required

# Create your views here.

#Allows user to join or create chatroom
def index(request):
	if request.method == 'POST':
		form = CreateChatRoomForm(request.POST)
		if form.is_valid():
			try:
				room = ChatRoom.objects.get(name=form.data['name'])
				return redirect('/chat/ws/' + str(room.key))
			except ChatRoom.DoesNotExist:
				newroom = ChatRoom(name=form.data['name'])
				newroom.save()
				newroom.users.add(request.user)
				return redirect('/chat/ws/' + str(newroom.key))
	else:
		form = CreateChatRoomForm()
	return render(request, 'chat/index.html', {'form' : form})

#Room
@login_required
def room(request, room_name):
	return render(request, 'chat/room.html', {
		'room_name': room_name
	})