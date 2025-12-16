from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

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
        return redirect(reverse('event_system:dashboard'))
    return redirect(reverse('event_system:dashboard'))
