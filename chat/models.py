from typing import ContextManager
from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
    displayName = models.CharField(max_length=255, blank=True, null=True)
    room = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000, unique=False, blank=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.content