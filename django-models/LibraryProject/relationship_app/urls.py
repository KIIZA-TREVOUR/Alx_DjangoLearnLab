# relationship_app/urls.py - Clean and working version
from django.urls import path
from . import views
from .views import list_books

app_name = 'relationship_app'

urlpatterns = [
    # Book and library views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    path('libraries/', views.LibraryListView.as_view(), name='library_list'),
    
    # Authentication views
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),    
    path('register/', views.registerView, name='register'),  
]