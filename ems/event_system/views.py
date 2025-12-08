from django.shortcuts import render

# Create your views here.
from django.views.generic import View
class HomePageView(View):
 def get(self, request):
    return render(request, 'event_system/home.html')
