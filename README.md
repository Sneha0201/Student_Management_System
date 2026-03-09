# Student Management System (Django)

A role-based web application built with Django to manage students and staff efficiently.

## Features

### Authentication
- Admin, Staff, and Student login system
- Role-based dashboard access

### Admin
- Manage Staff (Add, Edit, Delete)
- Manage Students (Add, Edit, Delete)
- Dashboard statistics
- Export students data to CSV

### Staff
- Staff dashboard
- View assigned students
- Staff profile

### Student
- Student dashboard
- Student profile
- View assigned staff

### Additional Features
- Search students
- Filter students by course
- Pagination
- Sidebar dashboard layout
- Template inheritance using `base.html`

## Technologies Used
- Python
- Django
- HTML
- SQLite
- Git & GitHub

## How to Run

```bash
git clone <repo-url>
cd Student_Management_System
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py runserver