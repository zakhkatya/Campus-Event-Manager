from django.contrib import admin
from django.contrib.auth.models import Group
from userauth.models import CustomUser
from .models import Event, Registration, Feedback


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff")
    fieldsets = (
        ("Overview", {"fields": ("username", "email", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Metadata", {"fields": ("id", "last_login", "date_joined")}),
        ("Avatar", {"fields": ("avatar",)}),
    )
    readonly_fields = ("id", "last_login", "date_joined")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date_start", "date_end", "location")
    readonly_fields = ("approved", "approved_at", "id")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "registered_at")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "rating")


try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass
