from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

# Helper: Check if user is Admin
def is_admin(user):
    return user.role == 'admin'

# Helper: Check if user is Admin or Organizer
def is_management(user):
    return user.role in ['admin', 'organizer']

class HomePageView(View):
   def get(self, request):
      return render(request, 'event_system/home.html')

class DashboardView(View):
   def get(self, request):
      return render(request, 'event_system/dashboard.html')
   
class MyEventsView(View):
   def get(self, request, *args, **kwargs):
      return render(request, 'event_system/events.html', {
         "title":"My events"
         # events 
      })

class UpcomingEventsView(View):
   def get(self, request, *args, **kwargs):
      return render(request, 'event_system/events.html', {
         "title":"Upcoming events"
         #events
      })

class NotificationsView(View):
   def get (self, request):
      return render(request, 'event_system/notifications.html')
   
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
        # Logic to update event status (approve/reject)
        print(f"Event {event_id} has been {status}ed")
        return redirect(reverse('event_system:dashboard'))
    return redirect(reverse('event_system:dashboard'))

