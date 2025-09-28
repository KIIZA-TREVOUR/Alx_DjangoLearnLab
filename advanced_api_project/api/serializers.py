from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    # Serializes the Book model.
    # Includes validation to ensure publication_year is not in the future.
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        # Ensure the publication year is not in the future.
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year {value} is in the future. Current year is {current_year}."
            )
        return value

class AuthorSerializer(serializers.ModelSerializer):
    # Serializes the Author model.
    # Includes a nested representation of all books written by this author.
    # The 'books' field uses BookSerializer to show full book details.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']