from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from .models import Book, Article
from .forms import BookForm, ArticleForm
from .forms import ExampleForm

# BOOK VIEWS - Secure implementation with Django forms and proper permission checks

@login_required
@csrf_protect
@permission_required('bookshelf.view_book', raise_exception=True)
def book_list(request):
    """View to list all books - requires view permission"""
    books = Book.objects.all().order_by('title')
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@csrf_protect
@permission_required('bookshelf.view_book', raise_exception=True)
def book_detail(request, pk):
    """Display details of a single book"""
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
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Book created successfully!')
                return redirect('book_list')
            except Exception as e:
                messages.error(request, "An error occurred while creating the book")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_create.html', {'form': form})

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
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Book updated successfully!')
                return redirect('book_detail', pk=book.pk)
            except Exception as e:
                messages.error(request, "An error occurred while updating the book")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_edit.html', {'form': form, 'book': book})

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
        form = ArticleForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    article = form.save(commit=False)
                    article.author = request.user
                    article.save()
                messages.success(request, 'Article created successfully!')
                return redirect('article_list')
            except Exception as e:
                messages.error(request, "An error occurred while creating the article")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ArticleForm()
    
    return render(request, 'bookshelf/article_create.html', {'form': form})

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
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Article updated successfully!')
                return redirect('article_detail', pk=article.pk)
            except Exception as e:
                messages.error(request, "An error occurred while updating the article")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ArticleForm(instance=article)
    
    return render(request, 'bookshelf/article_edit.html', {'form': form, 'article': article})

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
            with transaction.atomic():
                article.delete()
            messages.success(request, 'Article deleted successfully!')
            return redirect('article_list')
        except Exception as e:
            messages.error(request, "An error occurred while deleting the article")
    
    return render(request, 'bookshelf/article_delete.html', {'article': article})

# EXAMPLE FORM VIEW - Demonstrates secure form handling

@login_required
@csrf_protect
def example_form_view(request):
    """Example secure form view demonstrating Django security best practices"""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            messages.success(request, f'Thank you {name}! Your secure form submission was received.')
            return redirect('example_form_view')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})