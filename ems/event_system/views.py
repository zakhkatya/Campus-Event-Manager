from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Event, Registration, Notification
from django.db import transaction

User = get_user_model()

# Helper: Check if user is Admin
def is_admin(user):
    return user.role == 'admin'

# Helper: Check if user is Admin or Organizer
def is_management(user):
    return user.role in ['admin', 'organizer']

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        events = (
            Event.objects
            .filter(approved=True, is_private=False)
            .order_by("date")[:6]
        )
        return render(request, 'event_system/home.html', {
            "title": "Campus Event Manager",
            "events": events,
        })

class DashboardView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request):
        now = timezone.now()
        one_week_later = now + timedelta(days=7)
        stats = {}
        if request.user.role in ['admin', 'organizer']:
            stats = {
                'events_this_week': Event.objects.filter(date__range=[now, one_week_later], approved=True).count(),
                'events_total': Event.objects.count(),
                'students_registered': Registration.objects.values('user').distinct().count(),
                'students_total': User.objects.filter(role='student').count(),
                'organizers_total': User.objects.filter(role='organizer').count(),
                'organizers_active': User.objects.filter(role='organizer').count(), 
            }

        my_events = Registration.objects.filter(user=request.user).select_related("event")[:3]
        upcoming_events = Event.objects.filter(
            approved=True, 
            is_private=False,
            date__gte=now 
        ).order_by("-id")

        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:8]

        return render(request, "event_system/dashboard.html", {
            "title": "Admin Management Dashboard",
            "my_events": my_events,
            "upcoming_events": upcoming_events,
            "stats": stats,
            "notifications_list": notifications, 
        })
   
class MyEventsView(View):
   def get(self, request, *args, **kwargs):
      return render(request, 'event_system/events.html', {
         "title":"My events"
         # events 
      })

class UpcomingEventsView(View):
    def get(self, request, *args, **kwargs):
        events = (
            Event.objects
            .filter(approved=True, is_private=False)
            .order_by("-id")
        )
        return render(request, 'event_system/events.html', {
            "title": "Upcoming events",
            "events": events,
        })
class ApproveEventsListView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'admin'

    def get(self, request):
        pending_events = Event.objects.filter(approved=False).order_by("-id")
        
        return render(request, "event_system/approve_events.html", {
            "title": "Approve Events",
            "pending_events": pending_events,
        })


class NotificationsView(View):
   def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        
        return render(request, 'event_system/notifications.html', {
            "title": "My Notifications",
            "notifications_list": notifications,
        })
   
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def register_for_event(request, event_id):
    if request.method == 'POST':
        # Logic to join event goes here
        return redirect(reverse('event_system:dashboard'))
    return redirect(reverse('event_system:dashboard'))

@login_required
def unregister_from_event(request, event_id):
    if request.method == 'POST':
        # logic to unregister
        return redirect('event_system:dashboard')
    return redirect('event_system:dashboard')

@login_required
def delete_event(request, event_id):
    if request.user.role == 'admin' and request.method == 'POST':
        # logic to delete
        return redirect('event_system:dashboard')
    return redirect('event_system:dashboard')

@user_passes_test(is_management)
def add_event(request):
    if request.method == 'POST':
        # Logic to create event
        return redirect(reverse('event_system:dashboard'))
    return render(request, 'add_event.html')

@user_passes_test(is_admin)
def manage_status(request, event_id, status):
    if request.method == 'POST':
        with transaction.atomic():
            event = get_object_or_404(Event, id=event_id)
            if status == 'approve':
                event.is_private = False
                event.approved = True
                event.approved_at = timezone.now() 
                event.save()
                Notification.objects.create(
                    user=request.user,
                    message=f"Event #{event.id} approved."
                )

                other_users = User.objects.exclude(id=request.user.id)
                new_notifs = [
                    Notification(user=u, message=f"Event #{event.id} added.") 
                    for u in other_users
                ]
                Notification.objects.bulk_create(new_notifs)

        return redirect('event_system:dashboard') 
    return redirect('event_system:dashboard')

class EventDetailView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        is_registered = Registration.objects.filter(
            user=request.user,
            event=event
        ).exists()

        return render(
            request,
            "event_system/event_detail.html",
            {
                "event": event,
                "is_registered": is_registered,
                "registration": (
                    Registration.objects.filter(
                        user=request.user,
                        event=event
                    ).first()
                    if is_registered else None
                ),
            }
        )