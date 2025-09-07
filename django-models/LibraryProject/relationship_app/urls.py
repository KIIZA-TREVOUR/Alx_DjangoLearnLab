# relationship_app/urls.py
from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # Function-based view for listing books
    path('books/', views.list_books, name='list_books'),
    
    # Alternative function-based view for simple text output
    path('books/text/', views.list_books_text, name='list_books_text'),
    
    # Class-based view for library details
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Additional class-based view for listing all libraries
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Function-based alternative for library details
    path('library/detail/<int:pk>/', views.library_detail, name='library_detail_func'),
]