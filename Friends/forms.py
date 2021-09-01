from django import forms
from django.forms.forms import Form
from friendship.models import Friend, Follow, Block, FriendshipRequest # type: ignore

class AddFriendForm(forms.Form):
    forms.CharField(max_length=250, required=False)

    def save(self, sender, recipient, info):
        Friend.objects.add_friend(sender, recipient, message=info)

class AcceptFriendRequestForm(forms.Form):
    def save(self, sender, recipient):
        friend_request = FriendshipRequest.objects.get(to_user=recipient, from_user=sender)
        friend_request.accept()


class UnfriendForm(forms.Form):
    def save(self, sender, recipient):
        Friend.objects.remove_friend(sender, recipient)