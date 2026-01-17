import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

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

    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
    )

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

        if (
            old_avatar
            and self.avatar
            and old_avatar.name != self.avatar.name
            and old_avatar.name.startswith(f"avatars/{self.id}/")
        ):
            if os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)