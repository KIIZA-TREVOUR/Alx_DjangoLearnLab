from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Book
from .models import Article

@login_required
@permission_required('bookshelf.view_customuser', raise_exception=True)  # can adjust to your permission
def book_list(request):
    """View to list all books - requires view permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.view_customuser', raise_exception=True)
def book_detail(request, pk):
    """Display details of a single book"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """Create a new book - requires can_create permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year
        )
        messages.success(request, 'Book created successfully!')
        return redirect('book_list')
    return render(request, 'bookshelf/book_create.html')

@login_required
@permission_required('bookshelf.can_change', raise_exception=True)
def book_edit(request, pk):
    """Edit an existing book - requires can_change permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = request.POST.get('publication_year', book.publication_year)
        book.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('book_detail', pk=book.pk)
    return render(request, 'bookshelf/book_edit.html', {'book': book})

@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - requires can_delete permission"""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    return render(request, 'bookshelf/book_delete.html', {'book': book})

@login_required
@permission_required('app_name.can_view', raise_exception=True)
def article_list(request):
    """View to list all articles - requires can_view permission"""
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})

@login_required
@permission_required('app_name.can_view', raise_exception=True)
def article_detail(request, pk):
    """View to display article details - requires can_view permission"""
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/detail.html', {'article': article})

@login_required
@permission_required('app_name.can_create', raise_exception=True)
def article_create(request):
    """Create new article - requires can_create permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Article.objects.create(
            title=title,
            content=content,
            author=request.user
        )
        messages.success(request, 'Article created successfully!')
        return redirect('article_list')
    return render(request, 'articles/create.html')

@login_required
@permission_required('app_name.can_edit', raise_exception=True)
def article_edit(request, pk):
    """Edit existing article - requires can_edit permission"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.title = request.POST.get('title', article.title)
        article.content = request.POST.get('content', article.content)
        article.save()
        messages.success(request, 'Article updated successfully!')
        return redirect('article_detail', pk=article.pk)
    return render(request, 'articles/edit.html', {'article': article})

@login_required
@permission_required('app_name.can_delete', raise_exception=True)
def article_delete(request, pk):
    """Delete article - requires can_delete permission"""
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted successfully!')
        return redirect('article_list')
    return render(request, 'articles/delete.html', {'article': article})