from django.db import models
from django.conf import settings 
import uuid

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    ]


    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Event(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    date_start = models.DateTimeField(null=False, blank=False)
    date_end = models.DateTimeField(null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    category = models.CharField(max_length=100, null=False, blank=False)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events', default=None)

    is_private = models.BooleanField(default=False)    
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)      

    def __str__(self):
        return self.title

class Registration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"{self.user.username} → {self.event.title}"
    
    class Meta:
        unique_together = ("user", "event")

 
class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} rated {self.event.title}"
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}"