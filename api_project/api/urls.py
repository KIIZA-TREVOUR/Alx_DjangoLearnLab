from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet
from .auth_views import CustomAuthToken, register_user, logout_user, user_profile

# Create a router and register our ViewSet with it
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')

# Define the app name for namespacing
app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', CustomAuthToken.as_view(), name='login'),
    path('auth/token/', obtain_auth_token, name='obtain_token'),  # Alternative login endpoint
    path('auth/register/', register_user, name='register'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/profile/', user_profile, name='profile'),
    
    # Book endpoints
    path('books/', BookList.as_view(), name='book-list'),  # Simple list view (authenticated)
    
    # Include the router URLs for BookViewSet (all CRUD operations)
    path('', include(router.urls)),  # This includes all routes registered with the router
]