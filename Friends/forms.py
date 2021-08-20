from django import forms
from friendship.models import Friend, Follow, Block # type: ignore

class AddFriendForm(forms.Form):
    forms.CharField(max_length=250, required=False)

    def save(self, sender, recipient, info):
        Friend.objects.add_friend(sender, recipient, message=info)



class UnfriendForm:
    def save(self, sender, recipient):
        Friend.objects.remove_friend(sender, recipient)