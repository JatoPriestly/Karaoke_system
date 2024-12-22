from django.db import models

# Create your models here.

# user model
class User(AbstractUser):
    # Extend AbstractUser to include any additional fields needed
    display_name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.display_name or self.username