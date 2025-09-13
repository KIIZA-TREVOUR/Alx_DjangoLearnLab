from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


# -------------------------
# Author model
# -------------------------
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -------------------------
# Book model
# -------------------------
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
        ordering = ['title']


# -------------------------
# Library model
# -------------------------
class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name


# -------------------------
# UserProfile model
# -------------------------
class UserProfile(models.Model):
    """
    Extends the user model with roles and additional profile fields.
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='Member',
        help_text='User role that determines access permissions'
    )
    date_joined_profile = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# -------------------------
# Signals for automatic profile creation
# -------------------------
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a UserProfile automatically when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the UserProfile when the user is saved.
    """
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)
