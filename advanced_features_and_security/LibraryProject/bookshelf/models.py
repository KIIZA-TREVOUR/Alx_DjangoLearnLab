from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

class CustomUserManager(BaseUserManager):
    """
    Custom user manager that handles user creation with additional fields
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser with additional fields
    """
    
    # Make email the unique identifier instead of username
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional custom fields
    date_of_birth = models.DateField(
        _('date of birth'), 
        null=True, 
        blank=True,
        help_text=_('Enter your date of birth')
    )
    
    profile_photo = models.ImageField(
        _('profile photo'),
        upload_to='profile_photos/',
        null=True,
        blank=True,
        help_text=_('Upload a profile photo (optional)')
    )
    
    # Optional: Additional fields you might want to consider
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        help_text=_('Enter your phone number (optional)')
    )
    
    bio = models.TextField(
        _('bio'),
        max_length=500,
        blank=True,
        help_text=_('Tell us about yourself (optional)')
    )
    
    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username is still required for admin
    
    # Use the custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name
    
    @property
    def age(self):
        """
        Calculate and return the user's age based on date of birth
        """
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None