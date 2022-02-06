from turtle import title
from django import forms
from .models import ChatRoom, Message

class CreateChatRoomForm(forms.ModelForm):
    name = forms.CharField(max_length=100)

    class Meta:
        model = ChatRoom
        fields = ('name',)
