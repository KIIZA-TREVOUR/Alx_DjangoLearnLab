from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.contrib import messages
from .models import Article

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