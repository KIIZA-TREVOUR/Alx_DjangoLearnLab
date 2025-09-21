from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, help_text="The title of the book")
    author = models.CharField(max_length=100, help_text="The author of the book")
    publication_date = models.DateField(null=True, blank=True, help_text="Publication date")
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True, help_text="ISBN number")
    pages = models.PositiveIntegerField(null=True, blank=True, help_text="Number of pages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"