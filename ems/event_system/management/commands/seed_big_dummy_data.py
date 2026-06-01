from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from event_system.models import Event, Registration, Feedback, Category

User = get_user_model()

# =========================
# CONFIGURATION
# =========================
ORGANIZER_COUNT = 5
STUDENT_COUNT = 50
EVENT_COUNT = 120

REGISTRATIONS_PER_EVENT = (5, 40)
FEEDBACK_RATE = 0.5

NAMES = [
    "Alice", "Bob", "Charlie", "David", "Eva",
    "Frank", "Grace", "Hannah", "Ian", "Jack",
]

SURNAMES = [
    "Anderson", "Brown", "Clark", "Davis",
    "Evans", "Garcia", "Harris", "Johnson",
]

BANNERS = [
    "placeholder1.jpg",
    "placeholder2.jpg",
    "placeholder3.jpg",
]

avatar = "placeholder.webp"

DEFAULT_CATEGORIES = [
    "Workshop", "Seminar", "Conference", "Meetup", "Webinar"
]

class Command(BaseCommand):
    help = "Seed database with realistic demo data"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding database...")

        # -------------------------
        # CATEGORIES
        # -------------------------
        categories = []
        for name in DEFAULT_CATEGORIES:
            cat, _ = Category.objects.get_or_create(name=name)
            categories.append(cat)

        # -------------------------
        # ADMIN
        # -------------------------
        admin, created = User.objects.get_or_create(
            email="admin@example.com",
            defaults={
                "username": "admin",
                "is_staff": True,
                "is_superuser": True,
                "role": "admin",
                "first_name": "Admin",
                "last_name": "User",
                "avatar": avatar,
            },
        )
        if created:
            admin.set_password("admin123")
            admin.save()

        # -------------------------
        # ORGANIZERS
        # -------------------------
        organizers = []
        for i in range(1, ORGANIZER_COUNT + 1):
            user, created = User.objects.get_or_create(
                email=f"organizer{i}@example.com",
                defaults={
                    "username": f"organizer{i}",
                    "role": "organizer",
                    "first_name": random.choice(NAMES),
                    "last_name": random.choice(SURNAMES),
                    "avatar": avatar,
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
                    "role": "student",
                    "first_name": random.choice(NAMES),
                    "last_name": random.choice(SURNAMES),
                    "avatar": avatar,
                }
            )
            if created:
                user.set_password("password123")
                user.save()
            students.append(user)

        # -------------------------
        # EVENTS (past / current / future)
        # -------------------------
        events = []

        for i in range(1, EVENT_COUNT + 1):
            organizer = random.choice(organizers)
            category = random.choice(categories)
            banner = random.choice(BANNERS)

            time_type = random.choice(["past", "current", "future"])

            if time_type == "past":
                start = timezone.now() - timedelta(days=random.randint(10, 120))
            elif time_type == "current":
                start = timezone.now() - timedelta(hours=1)
            else:
                start = timezone.now() + timedelta(days=random.randint(5, 90))

            end = start + timedelta(hours=random.randint(1, 6))

            approved = random.choice([True, False])

            event = Event.objects.create(
                title=f"{category.name} #{i}",
                description="Automatically generated test event.",
                date_start=start,
                date_end=end,
                location=f"Room {random.randint(1, 50)}",
                category=category,
                organizer=organizer,
                banner=banner,
                is_private=random.choice([True, False]),
                approved=approved,
                approved_at=timezone.now() if approved else None,
            )
            events.append(event)

        # -------------------------
        # REGISTRATIONS
        # -------------------------
        registrations = []

        for event in events:
            if event.is_private:
                continue

            count = random.randint(*REGISTRATIONS_PER_EVENT)
            selected_students = random.sample(students, min(count, len(students)))

            for student in selected_students:
                reg, _ = Registration.objects.get_or_create(
                    user=student,
                    event=event,
                )
                registrations.append(reg)

        # -------------------------
        # FEEDBACK (only past events)
        # -------------------------
        feedback_count = 0
        for reg in registrations:
            if reg.event.date_end < timezone.now() and random.random() < FEEDBACK_RATE:
                Feedback.objects.get_or_create(
                    user=reg.user,
                    event=reg.event,
                    rating=random.randint(1, 5),
                    comment=random.choice([
                        "Great event!",
                        "Very useful.",
                        "Could be better.",
                        "Loved it!",
                        "Not bad.",
                    ])
                )
                feedback_count += 1

        # -------------------------
        # SUMMARY
        # -------------------------
        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully"))
        self.stdout.write(f"Categories: {len(categories)}")
        self.stdout.write(f"Organizers: {len(organizers)}")
        self.stdout.write(f"Students: {len(students)}")
        self.stdout.write(f"Events: {len(events)}")
        self.stdout.write(f"Registrations: {len(registrations)}")
        self.stdout.write(f"Feedback entries: {feedback_count}")
