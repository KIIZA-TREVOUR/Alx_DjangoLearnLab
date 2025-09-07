# relationship_app/views.py - Add these role-based views to your existing views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Book, Library, UserProfile

# Your existing views (keep all of these)...

def list_books(request):
    """Function-based view that displays all books in the database."""
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

def list_books_text(request):
    """Function-based view that returns a simple text list of books."""
    books = Book.objects.all().select_related('author')
    book_list = []
    for book in books:
        book_list.append(f"{book.title} by {book.author.name}")
    return HttpResponse("\n".join(book_list), content_type="text/plain")

class LibraryDetailView(DetailView):
    """Class-based view that displays details for a specific library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = self.object.books.count()
        return context

class LibraryListView(ListView):
    """Class-based view that displays all libraries."""
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

def library_detail(request, pk):
    """Function-based alternative to the class-based LibraryDetailView."""
    library = get_object_or_404(Library, pk=pk)
    return render(request, 'relationship_app/library_detail.html', {'library': library})

def registerView(request):
    """Function-based view for user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

class CustomLoginView(LoginView):
    """Custom login view using Django's built-in LoginView."""
    template_name = 'relationship_app/login.html'
    success_url = reverse_lazy('relationship_app:list_books')

class CustomLogoutView(LogoutView):
    """Custom logout view using Django's built-in LogoutView."""
    template_name = 'relationship_app/logout.html'

# ============================================
# NEW: ROLE-BASED ACCESS CONTROL VIEWS
# ============================================

# Helper functions to check user roles
def is_admin(user):
    """Check if user has Admin role."""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Admin'
    except UserProfile.DoesNotExist:
        return False

def is_librarian(user):
    """Check if user has Librarian role."""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Librarian'
    except UserProfile.DoesNotExist:
        return False

def is_member(user):
    """Check if user has Member role."""
    if not user.is_authenticated:
        return False
    try:
        return user.userprofile.role == 'Member'
    except UserProfile.DoesNotExist:
        return False

# Role-based views using @user_passes_test decorator

@user_passes_test(is_admin)
def admin_view(request):
    
    # Get statistics for admin dashboard
    total_books = Book.objects.count()
    total_libraries = Library.objects.count()
    total_users = UserProfile.objects.count()
    
    # Get role distribution
    admin_count = UserProfile.objects.filter(role='Admin').count()
    librarian_count = UserProfile.objects.filter(role='Librarian').count()
    member_count = UserProfile.objects.filter(role='Member').count()
    
    # Recent users (last 5)
    recent_users = UserProfile.objects.select_related('user').order_by('-date_joined_profile')[:5]
    
    context = {
        'total_books': total_books,
        'total_libraries': total_libraries,
        'total_users': total_users,
        'admin_count': admin_count,
        'librarian_count': librarian_count,
        'member_count': member_count,
        'recent_users': recent_users,
        'user_role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'Unknown'
    }
    
    return render(request, 'relationship_app/admin_view.html', context)

@user_passes_test(is_librarian)
def librarian_view(request):
    
    # Get library-specific data
    libraries = Library.objects.prefetch_related('books__author')
    books_without_library = Book.objects.filter(library__isnull=True)
    
    # Get recent additions (you might want to add date fields to your models)
    recent_books = Book.objects.select_related('author').order_by('-id')[:5]
    
    context = {
        'libraries': libraries,
        'books_without_library': books_without_library,
        'recent_books': recent_books,
        'total_libraries': libraries.count(),
        'total_books': Book.objects.count(),
        'user_role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'Unknown'
    }
    
    return render(request, 'relationship_app/librarian_view.html', context)

@user_passes_test(is_member)
def member_view(request):
    
    # Get data relevant to members
    all_books = Book.objects.select_related('author').order_by('title')
    all_libraries = Library.objects.prefetch_related('books')
    
    # Get some random book recommendations (simple implementation)
    import random
    recommended_books = list(Book.objects.select_related('author'))
    if len(recommended_books) > 3:
        recommended_books = random.sample(recommended_books, 3)
    
    context = {
        'all_books': all_books,
        'all_libraries': all_libraries,
        'recommended_books': recommended_books,
        'total_books': all_books.count(),
        'total_libraries': all_libraries.count(),
        'user_role': request.user.userprofile.role if hasattr(request.user, 'userprofile') else 'Unknown'
    }
    
    return render(request, 'relationship_app/member_view.html', context)


def check_role(request):
   
    #Helper view to check current user's role.
    
    if not request.user.is_authenticated:
        return render(request, 'relationship_app/role_check.html', {
            'message': 'You need to be logged in to check your role.',
            'user_role': None
        })
    
    try:
        user_profile = request.user.userprofile
        context = {
            'message': f'Your role is: {user_profile.role}',
            'user_role': user_profile.role,
            'username': request.user.username,
            'date_joined': user_profile.date_joined_profile
        }
    except UserProfile.DoesNotExist:
        context = {
            'message': 'No profile found. Please contact administrator.',
            'user_role': None
        }
    
    return render(request, 'relationship_app/role_check.html', context)