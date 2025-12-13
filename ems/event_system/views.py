from django.shortcuts import render
from django.views.generic import View

class HomePageView(View):
   def get(self, request):
      return render(request, 'event_system/home.html')

class DashboardView(View):
   def get(self, request):
      return render(request, 'event_system/dashboard.html')
   
class MyEventsView(View):
   def get(self, request, title):
      return render(request, 'event_system/events.html', {
         "My events":title,
         # events 
      })

class UpcomingEventsView(View):
   def get(self, request, title):
      return render(request, 'event_system/events.html', {
         "Upcoming events":title,
         #events
      })