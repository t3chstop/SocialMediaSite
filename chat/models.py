from operator import mod
from django.db import models
from django.conf import settings

# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=False, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    key = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, unique=False, blank=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.content