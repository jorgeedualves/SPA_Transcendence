from django.db import models
from django.conf import settings
from django.utils import timezone

class GameDB(models.Model):
    player1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='player1')
    player2 = models.CharField(max_length=100, blank=True, null=True)
    score_player1 = models.IntegerField()
    score_player2 = models.IntegerField()
    hits_player1 = models.IntegerField(default=0)
    duration = models.DurationField()
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Game on {self.date} between {self.player1} and {self.player2 or 'AI'}"