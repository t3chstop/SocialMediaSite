from os import truncate
from django.db import models
from django.conf import settings

# Create your models here.
class ChatRoom(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message", blank=True, null=True)
    room = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, unique=False, blank=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.content