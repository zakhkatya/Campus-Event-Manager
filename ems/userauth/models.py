from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(("email address"), unique=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'admin'
        super().save(*args, **kwargs)