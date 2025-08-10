from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', primary_key=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} profile'