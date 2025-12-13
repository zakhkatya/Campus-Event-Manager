from django.urls import path
from event_system.views import HomePageView, DashboardView, MyEventsView, UpcomingEventsView

app_name = 'event_system'
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("my-events", MyEventsView.as_view(), name="my-events" ),
    path("upcoming-events", UpcomingEventsView.as_view(), name="upcoming-events"),
]