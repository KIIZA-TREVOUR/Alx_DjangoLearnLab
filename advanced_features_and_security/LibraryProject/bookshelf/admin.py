from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import Book
from .models import CustomUser



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
    
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the custom user model
    """
    
    # The forms to add and change user instances
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    
    # The fields to be used in displaying the User model in admin
    list_display = (
        'email', 'username', 'first_name', 'last_name', 
        'is_staff', 'is_active', 'date_joined', 'profile_photo_preview'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups',
        'date_joined', 'last_login'
    )
    
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions')
    
    # Fieldsets for the change form
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'date_of_birth', 
                'phone_number', 'bio', 'profile_photo'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'first_name', 'last_name'
            ),
        }),
        (_('Additional Info'), {
            'classes': ('wide',),
            'fields': (
                'date_of_birth', 'phone_number', 'bio', 'profile_photo'
            ),
        }),
        (_('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login')
    
    def profile_photo_preview(self, obj):
        """
        Display a small preview of the profile photo in the admin list
        """
        if obj.profile_photo:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" />',
                obj.profile_photo.url
            )
        return "No photo"
    
    profile_photo_preview.short_description = 'Photo'
    
    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        
        if not is_superuser:
            # Non-superusers can't edit these fields
            disabled_fields = {'is_superuser', 'user_permissions'}
            
            for field in disabled_fields:
                if field in form.base_fields:
                    form.base_fields[field].disabled = True
        
        return form
    
    def save_model(self, request, obj, form, change):
        """
        Override save to handle any special processing
        """
        if not change:
            # This is a new user being created
            obj.set_password(obj.password)
        
        super().save_model(request, obj, form, change)


# Register the Book model with the custom admin class
admin.site.register(Book, BookAdmin)
# Register the custom user model with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)