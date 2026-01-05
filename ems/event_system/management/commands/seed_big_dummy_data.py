from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from event_system.models import Event, Registration, Feedback


User = get_user_model()

# =========================
# CONFIGURATION
# =========================
ORGANIZER_COUNT = 10
STUDENT_COUNT = 100
EVENT_COUNT = 300

REGISTRATIONS_PER_EVENT = (10, 30)  # min / max
FEEDBACK_RATE = 0.4  # 40% of registered users leave feedback

class Command(BaseCommand):
    help = "Seed database with a large interconnected dataset"

    def handle(self, *args, **options):
        self.stdout.write("Seeding BIG dummy dataset...")

        # -------------------------
        # ADMIN
        # -------------------------
        admin, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "username": "admin",
                "is_staff": True, 
                "is_superuser": True,
                "role": "admin"
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()
            self.stdout.write("Admin created.")

        # -------------------------
        # ORGANIZERS
        # -------------------------
        organizers = []
        for i in range(1, ORGANIZER_COUNT + 1):
            user, created = User.objects.get_or_create(
                email=f"organizer{i}@example.com",
                defaults={
                    "username": f"organizer{i}",
                    "role": "organizer"
                }
            )
            if created:
                user.set_password("password123")
                user.save()
            organizers.append(user)

        # -------------------------
        # STUDENTS
        # -------------------------
        students = []
        for i in range(1, STUDENT_COUNT + 1):
            user, created = User.objects.get_or_create(
                email=f"student{i}@example.com",
                defaults={
                    "username": f"student{i}",
                    "role": "student"
                }
            )
            if created:
                user.set_password("password123")
                user.save()
            students.append(user)

        # -------------------------
        # EVENTS
        # -------------------------
        categories = ["Workshop", "Lecture", "Party", "Sports", "Conference", "Meetup"]

        events = []
        for i in range(1, EVENT_COUNT + 1):
            organizer = random.choice(organizers)
            event = Event.objects.create(
                title=f"Event #{i}",
                description="Automatically generated test event.",
                date=timezone.now() + timedelta(days=random.randint(1, 180)),
                location=f"Building {random.randint(1, 20)}",
                category=random.choice(categories),
                is_private=random.choice([True, False]),
                approved=random.choice([True, False]),
                organizer=organizer,
            )
            events.append(event)

        # -------------------------
        # REGISTRATIONS
        # -------------------------
        registrations = []
        for event in events:
            reg_count = random.randint(REGISTRATIONS_PER_EVENT[0], REGISTRATIONS_PER_EVENT[1])
            selected_students = random.sample(students, k=min(reg_count, len(students)))

            for student in selected_students:
                registration, _ = Registration.objects.get_or_create(
                    user=student,
                    event=event,
                )
                registrations.append(registration)

        # -------------------------
        # FEEDBACK
        # -------------------------
        feedback_count = 0
        for registration in registrations:
            if random.random() < FEEDBACK_RATE:
                Feedback.objects.get_or_create(
                    user=registration.user,
                    event=registration.event,
                    rating=random.randint(1, 5),
                    comment=random.choice([
                        "Great event!", "Very useful.", "Could be better.", 
                        "Loved it!", "Not bad."
                    ]),
                )
                feedback_count += 1

        # -------------------------
        # SUMMARY
        # -------------------------
        self.stdout.write(self.style.SUCCESS("BIG dataset created successfully"))
        self.stdout.write(f"Admins: 1")
        self.stdout.write(f"Organizers: {ORGANIZER_COUNT}")
        self.stdout.write(f"Students: {STUDENT_COUNT}")
        self.stdout.write(f"Events: {EVENT_COUNT}")
        self.stdout.write(f"Registrations: {len(registrations)}")
        self.stdout.write(f"Feedback entries: {feedback_count}")