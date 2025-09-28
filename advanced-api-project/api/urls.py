from django.urls import path
from . import views

urlpatterns = [
    # List and detail (read-only)
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Write operations with explicit paths 
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'),
]