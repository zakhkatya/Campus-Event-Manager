from django.urls import path
from event_system.views import HomePageView, DashboardView, MyEventsView, UpcomingEventsView, NotificationsView, EventDetailView, registration_qr_view
from . import views

app_name = 'event_system'
urlpatterns = [
    # Home page
    path("", HomePageView.as_view(), name="home"),
    
    # Dashboard
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    
    # My Events
    path("my-events", MyEventsView.as_view(), name="my-events" ),
    
    # Upcoming Events
    path("upcoming-events", UpcomingEventsView.as_view(), name="upcoming-events"),
    
    # Notifications
    path("notifications", NotificationsView.as_view(), name="notifications"),
    
    # Event Details and Actions
    path("register/<int:event_id>/", views.register_for_event, name='register_event'),
    path('unregister/<int:event_id>/', views.unregister_from_event, name='unregister_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage/<int:event_id>/<str:status>/', views.manage_status, name='manage_event'),
    path("create/", views.event_create, name="event_create"),
    path("<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("event/<int:event_id>/", EventDetailView.as_view(), name="event_detail"),
    
    # Approval of Events
    path('approve-events/', views.ApproveEventsListView.as_view(), name='approve-events-list'),
    
    # Feedback Views
    path("my-feedback", views.MyFeedbacksView.as_view(), name="my-feedback"), 
    path("received-feedback", views.ReceivedFeedbacksView.as_view(), name="received-feedback"),
    path("submit_feedback/<int:event_id>", views.submit_feedback, name="submit_feedback"),
    
    # QR Code for Registrations
    path("registrations/<int:registration_id>/qr/", registration_qr_view, name="registration_qr"),
    
    # Past Events
    path("past-events", views.PastEventsView.as_view(), name="past-events"),

    # Ovents organized by the user
    path("organized-events", views.OrganizedEventsView.as_view(), name="organized-events"),
]