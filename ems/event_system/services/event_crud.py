from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.models import User
from event_system.models import Event, UserProfile


# --------------------
# HELPERS

# Check if user is admin
def _is_admin(user: User) -> bool:
    return user.is_staff or (
        hasattr(user, "userprofile") and user.userprofile.role == "admin"
    )

# Check if user is organizer
def _is_organizer(user: User) -> bool:
    return hasattr(user, "userprofile") and user.userprofile.role == "organizer"

# Check if user can manage events (organizer or admin)
def _can_manage_event(user: User) -> bool:
    return _is_admin(user) or _is_organizer(user)

# --------------------

# CREATE
def create_event(*, user: User, data: dict) -> Event:
    """
    Create a new event.
    Only organizer or admin can create events.
    """
    if not _can_manage_event(user):
        raise PermissionDenied("You are not allowed to create events.")

    event = Event(**data)
    event.full_clean()
    event.save()
    return event

# UPDATE
def update_event(*, user: User, event: Event, data: dict) -> Event:
    """
    Update an existing event.
    """
    if not _can_manage_event(user):
        raise PermissionDenied("You are not allowed to update events.")

    for field, value in data.items():
        if hasattr(event, field):
            setattr(event, field, value)

    event.full_clean()
    event.save()
    return event

