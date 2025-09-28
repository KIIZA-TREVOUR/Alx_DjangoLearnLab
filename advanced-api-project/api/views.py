from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookListView(generics.ListCreateAPIView):
    # View to list all books or create a new book using get and post.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Permission handled per method via custom logic or permission_classes
    def get_permissions(self):
        #returns the list of permissions that the view requires. Allow GET for everyone, require authentication for POST.
        
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    # View to retrieve, update, or delete a single book by ID by only authenticated users.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'  
    def get_permissions(self):
        # Allow GET for anyone; require authentication for PUT, PATCH, DELETE.
        if self.request.method == 'GET':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]