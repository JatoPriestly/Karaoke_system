from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# user model
class User(AbstractUser):
    display_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    # Explicitly define related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='karaoke_users',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='karaoke_users',
        blank=True,
    )

    def __str__(self):
        return self.display_name or self.username
    
    
# Song model
class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length= 200, blank=True, null=True)
    file_path = models.FileField(upload_to="songs/")
    lyrics_file =models.FileField(upload_to="lyrics/", blank=True, null=True) # For .lrc or similar files
    duration = models.PositiveIntegerField(blank=True, null=True) # Duration in seconds


    def __str__(self):
        return self.title
    

# DuetSession model
class DuetSession(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_sessions")
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="joined_sessions")
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.host} duet on {self.song.title}"

# Additional relations (if needed in the future)
# 1. User favorite songs
class FavoriteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorite_songs")
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} favorite {self.song}"

# 2. User duet history
class DuetHistory(models.Model):
    session = models.ForeignKey(DuetSession, on_delete=models.CASCADE, related_name="history")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recorded_audio = models.FileField(upload_to="recordings/", blank=True, null=True)
    performance_score = models.PositiveIntegerField(blank=True, null=True)  # Optional scoring

    def __str__(self):
        return f"{self.user} in {self.session}"
