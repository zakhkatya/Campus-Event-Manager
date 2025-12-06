from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)

    is_private = models.BooleanField(default=False)  # invitation-only
    approved = models.BooleanField(default=False)    # admin approval

    def __str__(self):
        return self.title

