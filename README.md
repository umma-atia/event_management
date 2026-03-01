# EventManager README.md

## Overview

EventManager is a comprehensive Django-based Event Management System designed to handle user registration, role-based access control, event creation, RSVP functionalities, and user profile management. It leverages Django ORM, optimized query techniques, Tailwind CSS for responsive design, and incorporates email verification, signals, and media management to deliver a robust platform.

---

## Features

- User authentication with email verification
- Role-based access control with Admin, Organizer, and Participant roles
- Event creation, update, deletion by authorized users
- RSVP system with email confirmation
- User profile management with profile picture and contact info
- User dashboards tailored to roles
- Media file handling for event images and profile pictures
- Signal-based notifications and processes

---

## Implementation Pattern

**EventManager** is implemented following Django's **Model-View-Template (MVT)** architectural pattern:

- **Models:** Define the data structure, including custom user models with profile pictures and phone numbers, event details, categories, RSVP relationships, and media fields.
- **Views:** Process user requests, enforce role-based access control, handle business logic, and interact with the models.
- **Templates:** Render the user interface, displaying dynamic content and forms, styled with Tailwind CSS for responsiveness.

This clear separation of concerns ensures a maintainable, scalable, and secure application structure.

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 4.x
- Tailwind CSS
- Email backend configured (SMTP settings)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/EventManager.git
cd EventManager
```

2. Create a virtual environment and activate it:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
# or
env\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

### Tailwind CSS Setup

Follow the Tailwind CSS documentation to integrate Tailwind with Django, or use `django-tailwind` package for seamless integration.

---

## Features Breakdown

### 1. Authentication

- **User Signup:** Register with username, email, password, first_name, last_name.
- **Login/Logout:** Standard Django auth views.
- **Email Activation:** Send activation email with a secure link; unactivated users cannot log in.
- **Password Reset:** Email-based password reset functionality.

### 2. Role-Based Access Control (RBAC)

- **Roles:** Admin, Organizer, Participant.
- **Implementation:** Use Django Groups.
- **Permissions:**
  - **Admin:** Full access; manage roles, groups, delete participants.
  - **Organizer:** Create, update, delete events and categories.
  - **Participant:** View events only.
- **Access Restrictions:** Decorators to restrict views based on roles.

### 3. RSVP System

- Participants can RSVP to events.
- RSVP stored using ManyToMany relationship.
- Prevent duplicate RSVP entries.
- Send confirmation email upon RSVP.
- Participant Dashboard to view RSVP’d events.

### 4. Email Activation

- Activation email sent post-registration.
- Secure activation links using Django's `default_token_generator`.
- Unactivated users cannot authenticate.

### 5. Django Signals & Media Files

- **Signals:**
  - Notify participants via email when they RSVP.
  - Send account activation email.
- **Media Files:**
  - Event images with default image.
  - Profile pictures with default image.

### 6. User Dashboards

- **Admin Dashboard:** Manage all entities.
- **Organizer Dashboard:** Manage events and categories.
- **Participant Dashboard:** View RSVP’d events.

### 7. Profile Features

- View profile.
- Edit profile details, including profile picture and phone number.
- Change password within profile.
- Password reset via email.

### 8. Custom User Model

- Extends Django's AbstractUser.
- Adds:
  - Profile picture (ImageField with default).
  - Phone number (validated CharField).
- Update authentication forms to use custom user.

---

## Code Structure

```
eventmanager/
│
├── accounts/               # Custom user model, forms, signals
├── events/                 # Event, Category, RSVP models and views
├── templates/              # HTML templates
├── static/                 # Tailwind CSS and static files
├── media/                  # Media uploads (images)
├── manage.py
├── requirements.txt
└── README.md
```

---

## Notes

- Ensure email backend is configured for email functionalities.
- Use Django admin to manage users and roles.
- Customize templates and static files for branding and responsiveness.
- Always test role-based access restrictions to ensure security.

---

## Future Enhancements

- Add notifications and reminders.
- Integrate with calendar APIs.
- Enable social authentication.
- Implement event comments and ratings.

---

## Support

For issues or feature requests, please open an issue on the GitHub repository or contact [your-email@example.com].

---

## License

This project is licensed under the MIT License.

---

*Thank you for using EventManager!*
