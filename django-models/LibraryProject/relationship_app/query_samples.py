from django.db import models
from relationship_app.models import Author, Book, Library, Librarian
# Query 1: All books by a specific author
def get_books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)
    return [book.title for book in books]

# Query 2: All books in a library
def get_books_in_library(library_name):
    books = Book.objects.filter(libraries__name=library_name)
    return [book.title for book in books]

# Query 3: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    librarian = Librarian.objects.filter(library__name=library_name).first()
    return librarian.name if librarian else f"No librarian found for {library_name}"
