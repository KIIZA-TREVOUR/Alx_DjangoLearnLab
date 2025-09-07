from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Book, Library

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that displays all books in the database.
    Returns a rendered template with a list of books and their authors.
    """
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Alternative function-based view for simple text output
def list_books_text(request):
    """
    Function-based view that returns a simple text list of books.
    This is a simpler version that returns plain text instead of HTML.
    """
    books = Book.objects.all().select_related('author')
    book_list = []
    for book in books:
        book_list.append(f"{book.title} by {book.author.name}")
    
    return HttpResponse("\n".join(book_list), content_type="text/plain")

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that displays details for a specific library.
    Shows the library name and all books available in that library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Optionally add extra context if needed
        context['total_books'] = self.object.books.count()
        return context

# Alternative class-based view using ListView for all libraries
class LibraryListView(ListView):
    """
    Class-based view that displays all libraries.
    This is an additional view that shows all libraries in the system.
    """
    model = Library
    template_name = 'relationship_app/library_list.html'
    context_object_name = 'libraries'
    
    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')

# Function-based view for library details (alternative implementation)
def library_detail(request, pk):
    """
    Function-based alternative to the class-based LibraryDetailView.
    Takes a library ID and displays the library details.
    """
    library = get_object_or_404(Library, pk=pk)
    return render(request, 'relationship_app/library_detail.html', {'library': library})