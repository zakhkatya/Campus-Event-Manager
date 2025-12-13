from django.shortcuts import render
from django.views.generic import View

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