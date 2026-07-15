from django.db import models
from django.contrib.auth.models import User

class Graph(models.Model):
    PLOT_TYPES = [
        ('line', 'Line'),
        ('bar', 'Bar'),
        ('pie', 'Pie'),
        ('scatter', 'Scatter'),
        ('box', 'Box'),
        ('3d', '3D Surface'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    plot_type = models.CharField(max_length=20, choices=PLOT_TYPES)
    data_json = models.JSONField()  # series, labels, colors, etc.
    image = models.ImageField(upload_to='graphs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title