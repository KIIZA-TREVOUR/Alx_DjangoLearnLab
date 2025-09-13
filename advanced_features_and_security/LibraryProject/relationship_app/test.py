# Run in Django shell: python manage.py shell
from django.contrib.auth.models import User
from relationship_app.models import UserProfile

def create_test_users():
    """Create test users for each role"""
    
    # Test data
    users_data = [
        ('admin_test', 'admin@example.com', 'testpass123', 'Admin'),
        ('librarian_test', 'librarian@example.com', 'testpass123', 'Librarian'),
        ('member_test', 'member@example.com', 'testpass123', 'Member'),
    ]
    
    for username, email, password, role in users_data:
        # Delete if exists
        User.objects.filter(username=username).delete()
        
        # Create user
        user = User.objects.create_user(username, email, password)
        
        # Set role
        profile = user.userprofile
        profile.role = role
        profile.save()
        
        print(f"✅ Created {role}: {username}")
    
    print("\n🧪 Test these credentials:")
    for username, email, password, role in users_data:
        print(f"  {role}: {username} / {password}")

# Run the function
create_test_users()