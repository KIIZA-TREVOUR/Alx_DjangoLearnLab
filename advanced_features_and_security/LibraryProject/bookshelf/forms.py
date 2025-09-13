from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re
from .models import Book, Article

class BookForm(forms.ModelForm):
    """
    Secure form for Book model with input validation and sanitization
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 200,
                'pattern': '[a-zA-Z0-9\\s\\-_.,!?]+',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'pattern': '[a-zA-Z\\s\\-.\']+',
                'placeholder': 'Enter author name'
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1000,
                'max': 2024,
                'placeholder': 'Enter publication year'
            })
        }
    
    def clean_title(self):
        """Security: Validate and sanitize book title"""
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError("Title is required.")
        
        # Security: Remove potentially dangerous characters
        title = escape(title.strip())
        
        # Validate title length
        if len(title) > 200:
            raise ValidationError("Title must be 200 characters or less.")
        
        # Security: Check for valid characters only
        if not re.match(r'^[a-zA-Z0-9\s\-_.,!?]+$', title):
            raise ValidationError("Title contains invalid characters. Only letters, numbers, and basic punctuation allowed.")
        
        return title
    
    def clean_author(self):
        """Security: Validate and sanitize author name"""
        author = self.cleaned_data.get('author')
        
        if not author:
            raise ValidationError("Author is required.")
        
        # Security: Remove potentially dangerous characters
        author = escape(author.strip())
        
        # Validate author length
        if len(author) > 100:
            raise ValidationError("Author name must be 100 characters or less.")
        
        # Security: Check for valid characters only (letters, spaces, hyphens, dots, apostrophes)
        if not re.match(r'^[a-zA-Z\s\-.\']+$', author):
            raise ValidationError("Author name contains invalid characters. Only letters, spaces, hyphens, dots, and apostrophes allowed.")
        
        return author
    
    def clean_publication_year(self):
        """Security: Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        
        if not year:
            raise ValidationError("Publication year is required.")
        
        # Security: Validate year range
        if year < 1000 or year > 2024:
            raise ValidationError("Publication year must be between 1000 and 2024.")
        
        return year

class ArticleForm(forms.ModelForm):
    """
    Secure form for Article model with input validation and sanitization
    """
    
    class Meta:
        model = Article
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 200,
                'pattern': '[a-zA-Z0-9\\s\\-_.,!?]+',
                'placeholder': 'Enter article title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': 5000,
                'rows': 8,
                'placeholder': 'Enter article content'
            })
        }
    
    def clean_title(self):
        """Security: Validate and sanitize article title"""
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError("Title is required.")
        
        # Security: Remove potentially dangerous characters
        title = escape(title.strip())
        
        # Validate title length
        if len(title) > 200:
            raise ValidationError("Title must be 200 characters or less.")
        
        # Security: Check for valid characters only
        if not re.match(r'^[a-zA-Z0-9\s\-_.,!?]+$', title):
            raise ValidationError("Title contains invalid characters. Only letters, numbers, and basic punctuation allowed.")
        
        return title
    
    def clean_content(self):
        """Security: Validate and sanitize article content"""
        content = self.cleaned_data.get('content')
        
        if not content:
            raise ValidationError("Content is required.")
        
        # Security: Remove potentially dangerous characters
        content = escape(content.strip())
        
        # Validate content length
        if len(content) > 5000:
            raise ValidationError("Content must be 5000 characters or less.")
        
        # Security: Basic content validation (allow more characters for content)
        if len(content) < 10:
            raise ValidationError("Content must be at least 10 characters long.")
        
        return content

class ExampleSecureForm(forms.Form):
    """
    Example form demonstrating Django security best practices
    """
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[a-zA-Z\\s\\-]+',
            'placeholder': 'Enter your name'
        }),
        help_text="Only letters, spaces, and hyphens allowed."
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        })
    )
    
    def clean_name(self):
        """Security: Validate and sanitize name field"""
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Name is required.")
        
        # Security: Escape HTML and remove dangerous characters
        name = escape(name.strip())
        
        # Security: Check for valid characters only
        if not re.match(r'^[a-zA-Z\s\-]+$', name):
            raise ValidationError("Name contains invalid characters. Only letters, spaces, and hyphens allowed.")
        
        return name
    
    def clean_message(self):
        """Security: Validate and sanitize message field"""
        message = self.cleaned_data.get('message')
        
        if not message:
            raise ValidationError("Message is required.")
        
        # Security: Escape HTML content
        message = escape(message.strip())
        
        # Basic length validation
        if len(message) < 5:
            raise ValidationError("Message must be at least 5 characters long.")
        
        return message