from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "content", "ISBN", "DDC", "date_added", "user")

    

# Register your models here.

admin.site.register(Book, BookAdmin)