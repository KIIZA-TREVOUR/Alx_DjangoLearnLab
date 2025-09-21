from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Create a router and register our ViewSet with it
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book')

app_name = 'api'

urlpatterns = [
    # Route for the BookList view (ListAPIView)
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)), 
]