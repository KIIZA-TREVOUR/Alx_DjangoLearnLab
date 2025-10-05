# Django Blog

A complete blog application built with Django featuring user authentication and full CRUD functionality for blog posts.

## Features
- **User Authentication**: Registration, login, logout, and profile management
- **Blog Post Management**: Create, view, edit, and delete posts
- **Permissions**: Only authors can edit or delete their own posts
- **Templates**: Clean, responsive UI using provided CSS and Bootstrap-like styling
- **Security**: CSRF protection, password hashing, and login-required views

## Setup
1. `python -m venv venv`
2. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
3. `pip install django`
4. `python manage.py migrate`
5. `python manage.py runserver`

Visit `http://127.0.0.1:8000` to use the application.