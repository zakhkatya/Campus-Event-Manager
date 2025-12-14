from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.models import User
from event_system.models import Event, UserProfile


# --------------------
# HELPERS
# --------------------

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


