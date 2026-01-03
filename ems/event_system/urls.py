from django.urls import path
from event_system.views import HomePageView, DashboardView, MyEventsView, UpcomingEventsView, NotificationsView, EventDetailView
from . import views

app_name = 'event_system'
urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("my-events", MyEventsView.as_view(), name="my-events" ),
    path("upcoming-events", UpcomingEventsView.as_view(), name="upcoming-events"),
    path("notifications", NotificationsView.as_view(), name="notifications"),
    path("register/<int:event_id>/", views.register_for_event, name='register_event'),
    path('unregister/<int:event_id>/', views.unregister_from_event, name='unregister_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage/<int:event_id>/<str:status>/', views.manage_status, name='manage_event'),
    path('add/', views.add_event, name='add_event'),
    path("event/<int:event_id>/", EventDetailView.as_view(), name="event_detail"),
    path('approve-events/', views.ApproveEventsListView.as_view(), name='approve-events-list'),
]