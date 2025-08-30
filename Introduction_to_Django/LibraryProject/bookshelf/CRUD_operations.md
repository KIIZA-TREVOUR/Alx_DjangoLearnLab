# CRUD Operations Documentation

This document contains all CRUD (Create, Read, Update, Delete) operations performed on the Book model using Django shell.

## Setup Commands
First, open the Django shell and import the necessary model:

```bash
python manage.py shell
```

```python
from bookshelf.models import Book
```

---

## CREATE Operation

### Command:
```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book.title} by {book.author} ({book.publication_year})")
print(f"Book ID: {book.id}")
```

### Output:
```
Book created: 1984 by George Orwell (1949)
Book ID: 1
```

### Verification:
```python
print(f"Total books in database: {Book.objects.count()}")
```

### Output:
```
Total books in database: 1
```

---

## RETRIEVE (READ) Operation

### Command:
```python
# Retrieve the specific book
book = Book.objects.get(title="1984")
print(f"Retrieved Book Details:")
print(f"ID: {book.id}")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

### Output:
```
Retrieved Book Details:
ID: 1
Title: 1984
Author: George Orwell
Publication Year: 1949
```



## UPDATE Operation

### Command:
```python
# Get the book to update
book = Book.objects.get(title="1984")
print(f"Original title: {book.title}")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated title: {book.title}")
```

### Output:
```
Original title: 1984
Updated title: Nineteen Eighty-Four
```

### Verification Command:
```python
# Verify the update
updated_book = Book.objects.get(id=1)
print(f"Verification - Book details after update:")
print(f"ID: {updated_book.id}")
print(f"Title: {updated_book.title}")
print(f"Author: {updated_book.author}")
print(f"Publication Year: {updated_book.publication_year}")
```

### Output:
```
Verification - Book details after update:
ID: 1
Title: Nineteen Eighty-Four
Author: George Orwell
Publication Year: 1949
```

---

## DELETE Operation

### Command:
```python
# Get the book to delete
book = Book.objects.get(title="Nineteen Eighty-Four")
book_title = book.title
book_id = book.id

# Delete the book
book.delete()
print(f"Book '{book_title}' (ID: {book_id}) has been deleted")
```

### Output:
```
Book 'Nineteen Eighty-Four' (ID: 1) has been deleted
```

### Output:
```
Total books remaining in database: 0
Remaining books:
  No books found
```

---

## Summary

All CRUD operations have been successfully performed:

1. ✅ **CREATE**: Created a Book instance with title "1984", author "George Orwell", and publication year 1949
2. ✅ **RETRIEVE**: Retrieved and displayed all attributes of the created book
3. ✅ **UPDATE**: Updated the book title from "1984" to "Nineteen Eighty-Four"
4. ✅ **DELETE**: Deleted the book and confirmed the deletion

## Commands to Exit Django Shell
```python
exit()
```
