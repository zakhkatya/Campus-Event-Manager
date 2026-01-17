from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Event, Registration, Feedback
from userauth.models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Feedback)

# Remove default Authentication and Authorization
admin.site.unregister(Group)