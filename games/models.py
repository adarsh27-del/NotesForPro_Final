# games/models.py
from django.db import models
from django.contrib.auth.models import User

class GameScore(models.Model):
    GAME_TYPES = [
        ('typing', 'Typing Mastery'),
        ('chess', 'Chess'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=20, choices=GAME_TYPES)
    score = models.PositiveIntegerField()
    details = models.JSONField(null=True, blank=True)  # wpm, accuracy, moves, winner, etc.
    played_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-played_at']

    def __str__(self):
        return f"{self.get_game_type_display()} – {self.score}"