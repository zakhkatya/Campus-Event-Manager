from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from event_system.models import UserProfile, Event, Registration, Feedback


# =========================
# KONFIGURACE
# =========================
ORGANIZER_COUNT = 10
STUDENT_COUNT = 100
EVENT_COUNT = 300

REGISTRATIONS_PER_EVENT = (10, 30)  # min / max
FEEDBACK_RATE = 0.4  # 40 % registrovaných zanechá feedback


class Command(BaseCommand):
    help = "Seed database with a large interconnected dataset"

    def handle(self, *args, **options):
        self.stdout.write("Seeding BIG dummy dataset...")

        # -------------------------
        # ADMIN
        # -------------------------
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )
        admin.set_password("admin123")
        admin.save()
        UserProfile.objects.get_or_create(user=admin, role="admin")

        # -------------------------
        # ORGANIZERS
        # -------------------------
        organizers = []
        for i in range(1, ORGANIZER_COUNT + 1):
            user, _ = User.objects.get_or_create(username=f"organizer{i}")
            user.set_password("password123")
            user.save()
            UserProfile.objects.get_or_create(user=user, role="organizer")
            organizers.append(user)

        # -------------------------
        # STUDENTS
        # -------------------------
        students = []
        for i in range(1, STUDENT_COUNT + 1):
            user, _ = User.objects.get_or_create(username=f"student{i}")
            user.set_password("password123")
            user.save()
            UserProfile.objects.get_or_create(user=user, role="student")
            students.append(user)

        # -------------------------
        # EVENTS
        # -------------------------
        categories = [
            "Workshop",
            "Lecture",
            "Party",
            "Sports",
            "Conference",
            "Meetup",
        ]

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
            )
            events.append(event)

        # -------------------------
        # REGISTRATIONS
        # -------------------------
        registrations = []
        for event in events:
            reg_count = random.randint(
                REGISTRATIONS_PER_EVENT[0],
                REGISTRATIONS_PER_EVENT[1],
            )
            selected_students = random.sample(
                students, k=min(reg_count, len(students))
            )

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
                    comment=random.choice(
                        [
                            "Great event!",
                            "Very useful.",
                            "Could be better.",
                            "Loved it!",
                            "Not bad.",
                        ]
                    ),
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
