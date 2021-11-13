from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message, ChatRoom

# Create your views here.
@login_required
def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    if not ChatRoom.objects.filter(title = room_name).exists():
        room = ChatRoom(title=room_name)
        room.save()
        room.users.add(request.user)
    displayName = request.user.display_name
    messages = Message.objects.filter(room = room_name)

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'displayName' : displayName,
        'messages' : messages,
    })

def rooms(request):
    rooms = ChatRoom.objects.filter(account = request.user)
    return render(request, 'chat/rooms.html', {
        'rooms' : rooms,
    })
