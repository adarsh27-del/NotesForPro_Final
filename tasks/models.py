# tasks/models.py
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title        = models.CharField(max_length=240)
    description  = models.TextField(blank=True)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority     = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    color        = models.CharField(max_length=9, default='#00D4FF')  # hex or hex+alpha
    deadline     = models.DateField(null=True, blank=True)
    order        = models.PositiveIntegerField(default=0, db_index=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        indexes = [models.Index(fields=['user', 'status'])]

    def __str__(self):
        return self.title