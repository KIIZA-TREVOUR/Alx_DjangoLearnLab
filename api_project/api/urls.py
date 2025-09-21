
from django.contrib import admin
from django.urls import path
from .views import BookList

app_name = 'api'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', BookList.as_view(), name='book-list'),
]
