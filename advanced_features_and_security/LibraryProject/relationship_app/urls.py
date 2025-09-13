from django.urls import path
from . import views
from .views import list_books

app_name = 'relationship_app'

urlpatterns = [
    # Existing book and library views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Existing authentication views
    path('login/', views.CustomLoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', views.CustomLogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.registerView, name='register'),
    
    # Existing role-based access control views
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    path('check-role/', views.check_role, name='check_role'),
    
    # NEW: Custom permission-protected book management URLs
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]