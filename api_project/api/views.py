from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    API view to retrieve a list of all books.
    
    This view extends ListAPIView which provides GET method handler
    for listing a queryset.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned books to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Book.objects.all()
        
        # Optional: Add filtering capabilities
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)
            
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
            
        return queryset.order_by('title')


class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing Book instances.
    
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    
    Available endpoints:
    - GET /books_all/ - List all books
    - POST /books_all/ - Create a new book
    - GET /books_all/{id}/ - Retrieve a specific book
    - PUT /books_all/{id}/ - Update a specific book (full update)
    - PATCH /books_all/{id}/ - Partial update a specific book
    - DELETE /books_all/{id}/ - Delete a specific book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def get_queryset(self):
        queryset = Book.objects.all()
        
        # Add filtering capabilities
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__icontains=author)
            
        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
            
        # Filter by publication year
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(publication_date__year=year)
            
        return queryset.order_by('title')
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'message': 'Book created successfully',
                'book': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a book with custom response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Book updated successfully',
            'book': serializer.data
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Book "{book_title}" deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        author = request.query_params.get('author', None)
        if not author:
            return Response(
                {'error': 'Author parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = self.queryset.filter(author__icontains=author)
        serializer = self.get_serializer(books, many=True)
        
        return Response({
            'author': author,
            'count': books.count(),
            'books': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def mark_favorite(self, request, pk=None):
        book = self.get_object()
        # In a real application, you might have a user favorite system
        return Response({
            'message': f'"{book.title}" marked as favorite',
            'book_id': book.id
        })
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'