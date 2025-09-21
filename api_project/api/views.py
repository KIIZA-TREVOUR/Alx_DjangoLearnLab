from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Book
from .serializers import BookSerializer
from .permissions import IsStaffOrReadOnly, IsAuthorOrReadOnly


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
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
    
    Authentication: Token authentication required
    Permissions: 
    - Read: Any authenticated user
    - Write: Staff users only
    
    Available endpoints:
    - GET /books_all/ - List all books (authenticated users)
    - POST /books_all/ - Create a new book (staff only)
    - GET /books_all/{id}/ - Retrieve a specific book (authenticated users)
    - PUT /books_all/{id}/ - Update a specific book (staff only)
    - PATCH /books_all/{id}/ - Partial update a specific book (staff only)
    - DELETE /books_all/{id}/ - Delete a specific book (staff only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]  # Staff can write, authenticated users can read
    
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
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            # Read-only actions: require authentication only
            permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Write actions: require staff permissions
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            # Default to staff permissions for custom actions
            permission_classes = [IsStaffOrReadOnly]
        
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                'message': 'Book created successfully',
                'book': serializer.data,
                'created_by': request.user.username
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Book updated successfully',
            'book': serializer.data,
            'updated_by': request.user.username
        })
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        book_title = instance.title
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Book "{book_title}" deleted successfully',
            'deleted_by': request.user.username
        }, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
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
            'books': serializer.data,
            'requested_by': request.user.username
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_favorite(self, request, pk=None):
        book = self.get_object()
        return Response({
            'message': f'"{book.title}" marked as favorite',
            'book_id': book.id,
            'marked_by': request.user.username
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def admin_stats(self, request):
        total_books = self.queryset.count()
        authors = self.queryset.values_list('author', flat=True).distinct()
        
        return Response({
            'total_books': total_books,
            'total_authors': len(authors),
            'authors': list(authors),
            'requested_by': request.user.username
        })


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]
    lookup_field = 'pk'