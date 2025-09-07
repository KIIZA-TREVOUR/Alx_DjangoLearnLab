from relationship_app.models import Author, Book, Library, Librarian

# Query 1: All books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        books = author.books.all()
        # Return from either (both are same logically)
        return [book.title for book in books]
    except Author.DoesNotExist:
        return f"No author named {author_name} found."


# Query 2: All books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = Book.objects.filter(libraries=library)
        return [book.title for book in books]
    except Library.DoesNotExist:
        return f"No library named {library_name} found."



# Query 3: The librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)  # ✅ required form
        return librarian.name
    except Library.DoesNotExist:
        return f"No library named {library_name} found."
    except Librarian.DoesNotExist:
        return f"No librarian assigned to {library_name}."