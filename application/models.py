# application/models.py
import uuid

from django.db import models

class Message(models.Model):
    text = models.TextField()
    username = models.CharField(max_length=100, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    message_id = models.CharField(
        max_length=255, unique=True, blank=False, null=False, default=uuid.uuid4
    )

    def __str__(self):
        return f"Message {self.message_id} by {self.username}"


class Reply(models.Model):
    message = models.ForeignKey(Message, related_name='replies', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply {self.id} to Message {self.message_id}"
