from django.contrib import admin
from .models import UserProfile, Event, Registration, Feedback

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Registration)
admin.site.register(Feedback)