# Campus Event Manager 🎓

The Campus Event Manager is a centralized web platform designed to make university events easier to discover, organize, and manage. It connects students, clubs, departments, and administrators in one simple and reliable system that handles everything from event creation to participation and feedback.

Students can browse upcoming campus events, register with a single click, receive reminders and updates, and share their experiences after attending. Clubs and departments can create and manage events, upload banners and details, track registrations, and view attendee feedback to improve future events. University administrators oversee the platform by managing users, approving events, and ensuring smooth operation across campus.

Powered by Django and PostgreSQL, the Campus Event Manager improves communication, reduces organizational effort, and encourages greater student engagement by bringing all campus activities into one accessible platform.

## Setup

1. git clone
2. docker compose up -d
3. docker compose exec ems_web python manage.py seed_big_dummy_data 
4. [Local server](http://localhost:8000/)

# Homepage
![Homepage](/docs/Homepage.jpeg)

# Dashboard
![Dashboard](/docs/Dashboard.jpeg)

# Admin Dashboard
![Admin Dashboard](/docs/Admin_dashboard.jpeg)

# Event Detail
![Event Detail](/docs/Event_detail.jpeg)

# Edit Event
![Edit Event](/docs/Edit_event.jpeg)

# Recieved Feedback
![Recieved Feedback](/docs/Recieved_feedback.jpeg)

# Dev Notes

## Make Migrations when changing Models
``` sh
docker compose exec ems_web python manage.py makemigrations
```
