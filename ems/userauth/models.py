import os
from django.db import models
from django.contrib.auth.models import AbstractUser

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    name = instance.first_name.lower().replace(" ", "_") if instance.first_name else "user"
    role = instance.role.lower() if instance.role else "student"
    filename = f"{name}_{role}_profile_photo.{ext}"

    return os.path.join('avatars/', filename)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    avatar = models.ImageField(upload_to=user_avatar_path, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)