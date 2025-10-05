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


## Comment System
- Authenticated users can add comments to any blog post
- Comment authors can edit or delete their own comments
- Comments are displayed directly on the post detail page
- Non-authenticated users can view comments but cannot add them

### Comment URLs
- `/post/<int:pk>/comments/new/` - Add comment to post
- `/comment/<int:pk>/update/` - Edit comment (author only)
- `/comment/<int:pk>/delete/` - Delete comment (author only)

## Advanced Features: Tagging and Search

### Tagging System
- Authors can add tags to posts during creation/editing
- Tags are entered as comma-separated values (e.g., "django, python, blog")
- Each tag becomes a clickable link that shows all posts with that tag
- Tags are case-insensitive and automatically created if they don't exist

### Search Functionality
- Search bar in the header searches across:
  - Post titles
  - Post content  
  - Tag names
- Search results show matching posts with previews
- Empty searches show "No posts found" message

### URLs
- `/tags/<tag_name>/` - View all posts with specific tag
- `/search/?q=keyword` - Search posts by keyword