from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Category, Event, Registration, Notification, Feedback
from django.db import transaction
from django.views.generic import ListView
from django.contrib import messages
import qrcode
from io import BytesIO
from django.http import HttpResponse
from userauth.forms import ProfileUpdateForm
from django.db.models import Count, Avg
from .forms import EventForm, FeedbackForm
import os

# Get the User model
User = get_user_model()

# Actual timezone-aware now
now = timezone.now()

# Helper: Check if user is Admin
def is_admin(user):
    return user.role == 'admin'

# Helper: Check if user is Admin or Organizer
def is_management(user):
    return user.role in ['admin', 'organizer']

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        
        events = (
            Event.objects
            .filter(approved=True, is_private=False, date_end__gte=now)
            .order_by("date_start")[:6]
        )
        return render(request, 'event_system/home.html', {
            "title": "Campus Event Manager",
            "events": events,
        })

class DashboardView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated

    def get(self, request):
        # Current time
        now = timezone.now()
        
        # Initialize stats
        stats = {}
        
        if request.user.role in ['admin', 'organizer']:
            stats = {
                'events_this_week': Event.objects.filter(date_start__range=[now, now + timedelta(days=7)], approved=True).count(),
                'events_total': Event.objects.count(),
                'students_registered': Registration.objects.values('user').distinct().count(),
                'students_total': User.objects.filter(role='student').count(),
                'organizers_total': User.objects.filter(role='organizer').count(),
                'organizers_active': User.objects.filter(role='organizer').count(), 
            }

        # Determine tab title based on role
        tab_title = "Admin Dashboard" if request.user.role == 'admin' else "Organizer Dashboard" if request.user.role == 'organizer' else "Student Dashboard"

        my_events = (
            Registration.objects
            .filter(user=request.user, event__date_end__gte=now) 
            .select_related('event')
            .order_by("event__date_start")
        )
        
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")[:8]

        upcoming_events = (
            Event.objects
            .filter(approved=True, is_private=False, date_end__gte=now)
            .order_by("date_start")[:12]
        )

        return render(request, "event_system/dashboard.html", {
            "title": tab_title,
            "my_events": my_events,
            "upcoming_events": upcoming_events,
            "stats": stats,
            "notifications_list": notifications, 
        })
   
class MyEventsView(View):
    def get(self, request, *args, **kwargs):

        category_id = request.GET.get("category")

        my_events = (
            Registration.objects
            .filter(
                user=request.user,
                event__date_end__gte=now
            )
            .select_related("event", "event__category")
            .order_by("event__date_start")
        )

        if category_id:
            my_events = my_events.filter(event__category_id=category_id)
            selected_category_name = Category.objects.filter(id=category_id).first()

        categories = (
            Category.objects
            .filter(
                events__registrations__user=request.user,
                events__date_end__gte=now
                )
            .distinct()
        )

        return render(request, 'event_system/events.html', {
            "title": "My events",
            "categories": categories,
            "events": [e.event for e in my_events],
            "events_count": my_events.count(),
            "selected_category": category_id,
            "selected_category_name": selected_category_name.name if category_id else None,
        })
    
# Events organized by the user
class OrganizedEventsView(View):
    def get(self, request, *args, **kwargs):

        category_id = request.GET.get("category")

        organized_events = (
            Event.objects
            .filter(organizer=request.user)
            .order_by("-date_start")
        )

        if category_id:
            organized_events = organized_events.filter(category_id=category_id)
            selected_category_name = Category.objects.filter(id=category_id).first()

        categories = (
            Category.objects
            .filter(events__organizer=request.user)
            .distinct()
        )

        return render(request, 'event_system/events.html', {
            "title": "Organized Events",
            "events": organized_events,
            "categories": categories,
            "events_count": organized_events.count(),
            "selected_category": category_id,
            "selected_category_name": selected_category_name.name if category_id else None,
        })
    
class UpcomingEventsView(View):
    def get(self, request, *args, **kwargs):

        category_id = request.GET.get("category")

        events = (
            Event.objects
            .filter(
                approved=True,
                is_private=False,
                date_end__gte=now
            )
            .order_by("date_start")
        )

        if category_id:
            events = events.filter(category_id=category_id)
            selected_category_name = Category.objects.filter(id=category_id).first()

        categories = (
            Category.objects
            .filter(events__approved=True, events__is_private=False, events__date_end__gte=now)
            .distinct()
        )

        return render(request, 'event_system/events.html', {
            "title": "Upcoming events",
            "events": events,
            "categories": categories,
            "events_count": events.count(),
            "selected_category": category_id,
            "selected_category_name": selected_category_name.name if category_id else None,
        })

class ApproveEventsListView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'admin'

    def get(self, request):
        pending_events = Event.objects.filter(approved=False).order_by("-id")
        
        return render(request, "event_system/approve_events.html", {
            "title": "Approve Events",
            "pending_events": pending_events,
        })

class NotificationsView(View):
   def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
        
        return render(request, 'event_system/notifications.html', {
            "title": "My Notifications",
            "notifications_list": notifications,
        })
   
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
        with transaction.atomic():
            event = get_object_or_404(Event, id=event_id)
            organizer = event.organizer
            
            if status == 'approve':
                event.is_private = False
                event.approved = True
                event.approved_at = timezone.now()
                event.save()

                messages.success(request, f"Event: {event.title} is now live.")
                Notification.objects.create(
                    user=organizer,
                    message=f"Your event '{event.title}' has been approved."
                )
                all_admins = User.objects.filter(role='admin')
                admin_notifs = [
                    Notification(
                        user=admin, 
                        message=f"Admin {request.user.get_full_name()} approved the event: {event.title}"
                    ) for admin in all_admins
                ]
                Notification.objects.bulk_create(admin_notifs)

            elif status == 'reject':
                event_title = event.title
                event.delete()

                messages.warning(request, f"Event: {event_title} has been rejected.")
                Notification.objects.create(
                    user=organizer,
                    message=f"Your event proposal '{event_title}' was rejected."
                )
                all_admins = User.objects.filter(role='admin')
                reject_notifs = [
                    Notification(
                        user=admin, 
                        message=f"Admin {request.user.get_full_name()} rejected the event proposal: {event_title}"
                    ) for admin in all_admins
                ]
                Notification.objects.bulk_create(reject_notifs)
                
        return redirect(request.META.get('HTTP_REFERER', 'event_system:dashboard'))
    return redirect('event_system:dashboard')

class EventDetailView(LoginRequiredMixin, View):
    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        now = timezone.now() 
        form = FeedbackForm()

        registration = Registration.objects.filter(
            user=request.user,
            event=event
        ).first()

        feedbacks = Feedback.objects.filter(
            event=event
        ).select_related("user").order_by("-created_at")

        avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0

        return render(
            request,
            "event_system/event_detail.html",
            {
                "event": event,
                "is_registered": bool(registration),
                "registration": registration,
                "title": event.title,
                "now": now,
                'form': form,
                'feedbacks' : feedbacks,
                "feedbacks_count" : feedbacks.count(),
                "avg_rating" : avg_rating,
            }
        )

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)

        if "register" in request.POST:
            Registration.objects.get_or_create(
                user=request.user,
                event=event,
            )

        elif "unregister" in request.POST:
            Registration.objects.filter(
                user=request.user,
                event=event,
            ).delete()

        return redirect("event_system:event_detail", event_id=event.id)
    
@login_required
def registration_qr_view(request, registration_id):
    registration = get_object_or_404(
        Registration,
        id=registration_id,
        user=request.user,
    )

    qr = qrcode.make(str(registration.uuid))
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    return HttpResponse(
        buffer.getvalue(),
        content_type="image/png"
    )

class MyFeedbacksView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'event_system/my_feedback.html'
    context_object_name = 'feedbacks'

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user).select_related('event').order_by("-created_at")

class ReceivedFeedbacksView(UserPassesTestMixin, ListView):
    model = Event
    template_name = 'event_system/received_feedback.html'
    context_object_name = 'events_with_feedbacks'
    paginate_by = 10

    def test_func(self):
        return self.request.user.role in ['admin', 'organizer']

    def get_queryset(self):
        user = self.request.user
        view_filter = self.request.GET.get('filter')
    
        queryset = Event.objects.filter(feedback__isnull=False).annotate(
            total_comments=Count('feedback'),
            avg_rating=Avg('feedback__rating')
        ).prefetch_related('feedback_set', 'feedback_set__user').distinct()
        
        if user.role == 'admin':
            if view_filter == 'my_events':
                queryset = queryset.filter(organizer=user)
        else:
            queryset = queryset.filter(organizer=user)
            
        return queryset.order_by("-date_start")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        return context

@login_required
def submit_feedback(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        comment = request.POST.get('comment')
        rating = request.POST.get('rating', 5)

        Feedback.objects.create(
            user=request.user,
            event=event,
            comment=comment,
            rating=int(rating)
        )
        Notification.objects.create(
            user=event.organizer,
            message=f"New feedback received for your event: '{event.title}'"
        )
        
        return redirect('event_system:event_detail', event_id=event_id)
    return redirect('event_system:dashboard')


@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("userauth:edit-profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, "userauth/edit_profile.html", {"form": form})


class PastEventsView(View):
    def get(self, request, *args, **kwargs):
        now = timezone.now()
        category_id = request.GET.get("category")
        past_events = Event.objects.filter(
            date_end__lt=now, 
            approved=True
        ).order_by("-date_end")

        if category_id:
            past_events = past_events.filter(category_id=category_id)
            categories = Category.objects.filter(id=category_id).first()
            selected_category_name = Category.objects.filter(id=category_id).first()

        categories = (Category.objects.filter(events__date_end__lte=now).distinct()
        )
        
        return render(request, 'event_system/events.html', {
            "title": "Past Events",
            "events": past_events,
            "categories": categories,
            "events_count": past_events.count(),
            "selected_category": category_id,
            "selected_category_name": selected_category_name.name if category_id else None,
        })
    
@user_passes_test(is_management)
def event_create(request):
    form = EventForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        return redirect("event_system:event_detail", event.id)

    return render(request, "event_system/event_form.html", {
        "form": form,
        "event": None,
        "is_create": True,
    })

@user_passes_test(is_management)
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)

    old_banner = event.banner

    form = EventForm(
        request.POST or None,
        request.FILES or None,
        instance=event
    )

    if form.is_valid():
        event = form.save(commit=False)

        if "banner-clear" in request.POST:
            if (
                old_banner
                and old_banner.name.startswith(f"banners/{event.id}/")
                and os.path.isfile(old_banner.path)
            ):
                os.remove(old_banner.path)

            event.banner = None

        elif (
            old_banner
            and event.banner
            and old_banner.name != event.banner.name
            and old_banner.name.startswith(f"banners/{event.id}/")
        ):
            if os.path.isfile(old_banner.path):
                os.remove(old_banner.path)

        event.save()

        # Notification to organizer about the update
        Notification.objects.create(
            user=event.organizer,
            message=f"Details for your event '{event.title}' have been successfully updated."
        )

        # Notifications to registered users about the update
        registrations = event.registrations.select_related("user")
        Notification.objects.bulk_create([
            Notification(
                user=reg.user,
                message=f"Update: The details for '{event.title}' have changed. Please check the event page."
            )
            for reg in registrations
        ])

        return redirect("event_system:event_detail", event.id)

    return render(request, "event_system/event_form.html", {
        "form": form,
        "event": event,
        "is_create": False,
    })