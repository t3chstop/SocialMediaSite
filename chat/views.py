from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message, ChatRoom

# Create your views here.
@login_required
def index(request):
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    try:
        room = ChatRoom.objects.get(title=room_name)
    except:
        return HttpResponse("That room does not exist")
        
    #Check if user is authorized to view room
    if request.user in room.users.all():
        displayName = request.user.display_name
        messages = Message.objects.filter(room = room_name)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'displayName' : displayName,
            'messages' : messages,
        })
    else:
        return HttpResponse("You are not authorized to view this room")
        


def rooms(request):
    rooms = ChatRoom.objects.filter(users__display_name=request.user.display_name)
    return render(request, 'chat/rooms.html', {
        'rooms' : rooms,
    })
