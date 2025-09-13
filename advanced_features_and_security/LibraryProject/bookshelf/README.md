# Django Permissions and Groups System

## Overview
This Django application implements a role-based access control system using custom permissions and user groups to manage access to Article operations.

## Custom Permissions
The following permissions are defined in the Article model:
- `can_view` - View articles
- `can_create` - Create new articles
- `can_edit` - Edit existing articles
- `can_delete` - Delete articles

## User Groups Configuration

### Viewers
- **Permissions**: `can_view`
- **Access**: Read-only access to articles

### Editors
- **Permissions**: `can_view`, `can_create`, `can_edit`
- **Access**: Can view, create, and modify articles

### Admins
- **Permissions**: `can_view`, `can_create`, `can_edit`, `can_delete`
- **Access**: Full CRUD operations on articles

## Permission Enforcement
All views use the `@permission_required` decorator to enforce access control:
- Users without required permissions receive 403 Forbidden errors
- All views require user authentication via `@login_required`
- Replace `app_name` in permission strings with your actual Django app name

## Setup Instructions
1. Run migrations: `python manage.py makemigrations && python manage.py migrate`
2. Create groups in Django Admin at `/admin/auth/group/`
3. Assign permissions to groups as defined above
4. Create users and assign them to appropriate groups

## Testing
Create test users in each group and verify permission enforcement by attempting to access different views while logged in as each user type.