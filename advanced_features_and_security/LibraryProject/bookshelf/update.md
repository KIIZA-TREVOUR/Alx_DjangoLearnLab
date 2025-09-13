# Command
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Book title updated to: {book.title}")
```

# Expected Output
```python
Book title updated to: Nineteen Eighty-Four
```