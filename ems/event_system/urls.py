from django.urls import path
from event_system.views import HomePageView, DashboardView, MyEventsView, UpcomingEventsView, NotificationsView, EventDetailView, registration_qr_view
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
    path("my-feedbacks", views.MyFeedbacksView.as_view(), name="my-feedback"), 
    path("received-feedbacks", views.ReceivedFeedbacksView.as_view(), name="received-feedback"),
    path("registrations/<int:registration_id>/qr/", registration_qr_view, name="registration_qr"),
    path("past-events", views.PastEventsView.as_view(), name="past-events"),
]