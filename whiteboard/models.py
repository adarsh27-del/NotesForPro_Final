from django.db import models
from django.contrib.auth.models import User

class Whiteboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='whiteboards')
    title = models.CharField(max_length=150, default="Canvas")
    strokes_json = models.JSONField(null=True, blank=True)
    preview_image = models.ImageField(upload_to='whiteboards/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"