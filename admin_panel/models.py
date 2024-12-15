# admin_panel/models.py
from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=200,)
    content = models.TextField()
    link = models.URLField(max_length=500, blank=True)
    venue = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_panel_blogs')

    def __str__(self):
        return self.title
