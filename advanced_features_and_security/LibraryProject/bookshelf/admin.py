from django.contrib import admin
from .models import Book
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # Display these fields in the admin list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters in the right sidebar
    list_filter = ('author', 'publication_year')
    
    # Add search functionality
    search_fields = ('title', 'author')
    
    # Optional: Add ordering
    ordering = ('title',)
    
    # Optional: Add fields to be displayed in the detail view
    fields = ('title', 'author', 'publication_year')
    
    # Optional: Set how many items to show per page
    list_per_page = 20
    
    # Optional: Enable actions on the change list page
    actions_on_top = True
    actions_on_bottom = True
    

# Register the Book model with the custom admin class
admin.site.register(Book, BookAdmin)