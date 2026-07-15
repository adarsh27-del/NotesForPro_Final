from django.db import models
from django.contrib.auth.models import User


class AIResult(models.Model):
    TOOL_TYPES = [
        ('summarize', 'Summarize'),
        ('translate', 'Translate'),
        ('generate', 'Generate'),
        ('ocr', 'OCR'),
        ('meeting-notes', 'Meeting Notes'),
        ('generate-image','Image Generation')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tool_type = models.CharField(max_length=20, choices=TOOL_TYPES)
    prompt = models.TextField(blank=True)
    input_file = models.FileField(upload_to='ai_input/', null=True, blank=True)
    output_text = models.TextField(blank=True)
    output_file = models.FileField(upload_to='ai_output/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tool_type_display()} – {self.created_at.strftime('%Y-%m-%d %H:%M')}"