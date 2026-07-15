from django.db import models
from django.conf import settings


class MindMap(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mindmaps"
    )

    title = models.CharField(max_length=200)

    central = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    structure_json = models.JSONField(
        default=dict,
        blank=True
    )

    svg_content = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Mind Maps"

    def __str__(self):
        return f"{self.title} – {self.user}"