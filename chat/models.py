from typing import ContextManager
from django.db import models
from django.conf import settings

# Create your models here.
class chatRoom(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

    def connect(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added

    def disconnect(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        return f"chatRoom-{self.id}"

class MessageManager(models.Manager):
    def byRoom(self, room):
        qs = Message.objects.filter(room=room).order_by("-timestamp")
        return qs

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(chatRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, unique=False, blank=True)

    objects = MessageManager

    def __str__(self):
        return self.content