from django.db import models
from api.models import Room

# Create your models here.
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=150)
    refresh_token = models.CharField(max_length=150, null=True)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

class Vote(models.Model):
    user = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    song_id = models.CharField(max_length=50, null=True)
