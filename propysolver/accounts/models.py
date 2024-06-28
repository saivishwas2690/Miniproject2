from django.db import models
from django.contrib.auth.models import AbstractUser

class ProPyUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True, null = False, blank = False)
    email = models.EmailField(unique=True, null = False, blank = False)

    

class Profile(models.Model):
    user = models.OneToOneField(ProPyUser, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True, default="No bio")





