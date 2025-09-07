from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_year = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        # Custom permissions for the Book model
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
        
        # Additional metadata
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['title']  # Default ordering by title

class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, blank=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """
    UserProfile model that extends Django's built-in User model.
    Adds role-based access control with predefined roles.
    """
    
    # Role choices
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'), 
        ('Member', 'Member'),
    ]
    
    # One-to-One relationship with Django's User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Role field with predefined choices
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='Member',
        help_text='User role that determines access permissions'
    )
    
    # Optional: Additional profile fields
    date_joined_profile = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

# Django Signal to automatically create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler that automatically creates a UserProfile 
    when a new User is registered.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)  
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler that saves the UserProfile when User is saved.
    """
    # Check if UserProfile exists, create if it doesn't
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)