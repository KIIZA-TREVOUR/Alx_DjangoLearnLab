from rest_framework import serializers
from .models import Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model
        # You can also add extra configurations
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookDetailSerializer(BookSerializer):
    class Meta(BookSerializer.Meta):
        # Inherit from BookSerializer but can add custom behavior
        pass
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add computed field for display purposes
        data['display_name'] = f"{instance.title} by {instance.author}"
        return data