from django.urls import path
from event_system.views import HomePageView, DashboardView

app_name = 'event_system'
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
]