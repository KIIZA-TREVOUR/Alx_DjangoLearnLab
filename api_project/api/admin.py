from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_date', 'isbn', 'pages', 'created_at']
    list_filter = ['publication_date', 'created_at', 'author']
    search_fields = ['title', 'author', 'isbn']
    ordering = ['title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'publication_date')
        }),
        ('Details', {
            'fields': ('isbn', 'pages'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )