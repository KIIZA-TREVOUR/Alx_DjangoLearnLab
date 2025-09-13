from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django.db import transaction
import re
from .models import Book, Article

# Security: Input validation functions
def validate_year(year):
    """Validate publication year input"""
    try:
        year_int = int(year)
        if year_int < 1000 or year_int > 2024:
            raise ValidationError("Publication year must be between 1000 and 2024")
        return year_int
    except (ValueError, TypeError):
        raise ValidationError("Publication year must be a valid number")

def sanitize_text_input(text, max_length=200):
    """Sanitize and validate text input"""
    if not text or not isinstance(text, str):
        raise ValidationError("Invalid text input")
    
    # Remove potentially dangerous characters
    sanitized = escape(text.strip())
    
    if len(sanitized) > max_length:
        raise ValidationError(f"Text too long. Maximum {max_length} characters allowed")
    
    return sanitized

# BOOK VIEWS - Secure implementation with proper permission checks
@login_required
@csrf_protect
@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    """View to list all books - requires view permission"""
    # Security: Use ORM queries to prevent SQL injection
    books = Book.objects.all().order_by('title')
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@csrf_protect
@permission_required('bookshelf.view_book', raise_exception=True)
def book_detail(request, pk):
    """Display details of a single book"""
    # Security: Validate pk parameter and use get_object_or_404
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, "Invalid book ID")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@csrf_protect
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """Create a new book - requires can_create permission"""
    if request.method == 'POST':
        try:
            # Security: Validate and sanitize all inputs
            title = sanitize_text_input(request.POST.get('title'), 200)
            author = sanitize_text_input(request.POST.get('author'), 100)
            publication_year = validate_year(request.POST.get('publication_year'))
            
            # Security: Use transaction to ensure data integrity
            with transaction.atomic():
                Book.objects.create(
                    title=title,
                    author=author,
                    publication_year=publication_year
                )
            
            messages.success(request, 'Book created successfully!')
            return redirect('book_list')
            
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, "An error occurred while creating the book")
    
    return render(request, 'bookshelf/book_create.html')

@login_required
@csrf_protect
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """Edit an existing book - requires can_edit permission"""
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, "Invalid book ID")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            # Security: Validate and sanitize all inputs
            title = sanitize_text_input(request.POST.get('title', book.title), 200)
            author = sanitize_text_input(request.POST.get('author', book.author), 100)
            publication_year = validate_year(request.POST.get('publication_year', book.publication_year))
            
            # Security: Use transaction for atomic updates
            with transaction.atomic():
                book.title = title
                book.author = author
                book.publication_year = publication_year
                book.save()
            
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
            
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, "An error occurred while updating the book")
    
    return render(request, 'bookshelf/book_edit.html', {'book': book})

@login_required
@csrf_protect
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - requires can_delete permission"""
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, "Invalid book ID")
        return redirect('book_list')
    
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            # Security: Use transaction for safe deletion
            with transaction.atomic():
                book.delete()
            messages.success(request, 'Book deleted successfully!')
            return redirect('book_list')
        except Exception as e:
            messages.error(request, "An error occurred while deleting the book")
    
    return render(request, 'bookshelf/book_delete.html', {'book': book})

# ARTICLE VIEWS - Secure implementation
@login_required
@csrf_protect
@permission_required('bookshelf.can_view', raise_exception=True)
def article_list(request):
    """View to list all articles - requires can_view permission"""
    # Security: Use ORM with proper ordering to prevent SQL injection
    articles = Article.objects.select_related('author').order_by('-created_at')
    return render(request, 'bookshelf/article_list.html', {'articles': articles})

@login_required
@csrf_protect
@permission_required('bookshelf.can_view', raise_exception=True)
def article_detail(request, pk):
    """View to display article details - requires can_view permission"""
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, "Invalid article ID")
        return redirect('article_list')
    
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'bookshelf/article_detail.html', {'article': article})

@login_required
@csrf_protect
@permission_required('bookshelf.can_create', raise_exception=True)
def article_create(request):
    """Create new article - requires can_create permission"""
    if request.method == 'POST':
        try:
            # Security: Validate and sanitize inputs
            title = sanitize_text_input(request.POST.get('title'), 200)
            content = sanitize_text_input(request.POST.get('content'), 5000)
            
            # Security: Use transaction for atomic creation
            with transaction.atomic():
                Article.objects.create(
                    title=title,
                    content=content,
                    author=request.user
                )
            
            messages.success(request, 'Article created successfully!')
            return redirect('article_list')
            
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, "An error occurred while creating the article")
    
    return render(request, 'bookshelf/article_create.html')

@login_required
@csrf_protect
@permission_required('bookshelf.can_edit', raise_exception=True)
def article_edit(request, pk):
    """Edit existing article - requires can_edit permission"""
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, "Invalid article ID")
        return redirect('article_list')
    
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        try:
            # Security: Validate and sanitize inputs
            title = sanitize_text_input(request.POST.get('title', article.title), 200)
            content = sanitize_text_input(request.POST.get('content', article.content), 5000)
            
            # Security: Use transaction for atomic updates
            with transaction.atomic():
                article.title = title
                article.content = content
                article.save()
            
            messages.success(request, 'Article updated successfully!')
            return redirect('article_detail', pk=article.pk)
            
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
        except Exception as e:
            messages.error(request, "An error occurred while updating the article")
    
    return render(request, 'bookshelf/article_edit.html', {'article': article})

@login_required
@csrf_protect
@permission_required('bookshelf.can_delete', raise_exception=True)
def article_delete(request, pk):
    """Delete article - requires can_delete permission"""
    try:
        pk = int(pk)
    except (ValueError, TypeError):
        messages.error(request, "Invalid article ID")
        return redirect('article_list')
    
    article = get_object_or_404(Article, pk=pk)
    
    if request.method == 'POST':
        try:
            # Security: Use transaction for safe deletion
            with transaction.atomic():
                article.delete()
            messages.success(request, 'Article deleted successfully!')
            return redirect('article_list')
        except Exception as e:
            messages.error(request, "An error occurred while deleting the article")
    
    return render(request, 'bookshelf/article_delete.html', {'article': article})