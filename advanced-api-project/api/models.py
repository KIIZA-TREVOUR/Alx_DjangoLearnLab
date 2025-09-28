from django.db import models

class Author(models.Model):
    # Represents an author with a name.
    # An author can write multiple books (one-to-many relationship).
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Represents a book with a title, publication year, and associated author.
    # Each book belongs to one author.
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"