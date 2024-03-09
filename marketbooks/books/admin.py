from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, CustomUserAdmin)  # Register User with custom admin

from .models import Book, BooksCategory

# Register your models here.
admin.site.register(Book)
admin.site.register(BooksCategory)
