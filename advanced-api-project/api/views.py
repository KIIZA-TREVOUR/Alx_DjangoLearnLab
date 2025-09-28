from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters  # for search and ordering
from django_filters.rest_framework import DjangoFilterBackend  # for filtering
from .models import Book
from .serializers import BookSerializer

# Show all books - anyone can see with  filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Add filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Fields you can filter by (exact match)
    filterset_fields = ['title', 'publication_year', 'author']
    # Fields you can search in (text search)
    search_fields = ['title', 'author__name']
    # Fields you can order by
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default order

# See one book - anyone can see
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Add a new book - only logged-in users
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Change a book - only logged-in users
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# Remove a book - only logged-in users
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]