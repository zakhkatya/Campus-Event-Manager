import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy

def user_avatar_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return f"avatars/{instance.id}/avatar.{ext}"

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("organizer", "Organizer"),
        ("admin", "Admin"),
    ]

    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=150, unique=False, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    avatar = CloudinaryField('image', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

def save(self, *args, **kwargs):
    old_avatar = None

    if self.pk:
        try:
            old_avatar = CustomUser.objects.get(pk=self.pk).avatar
        except CustomUser.DoesNotExist:
            pass

    if self.is_superuser:
        self.role = "admin"

    super().save(*args, **kwargs)

    if old_avatar and self.avatar:
        old_public_id = getattr(old_avatar, 'public_id', None)
        new_public_id = getattr(self.avatar, 'public_id', None)

        if old_public_id and old_public_id != new_public_id:

            if old_public_id.startswith(f"{self.id}/"):
                try:
                    destroy(old_public_id)
                except Exception:
                    pass
            
            elif hasattr(old_avatar, 'path') and os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)