# Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book_title = book.title  
book.delete()
print(f"Book '{book_title}' has been deleted")
```

# Expected Output
```python
Book 'Nineteen Eighty-Four' has been deleted
```