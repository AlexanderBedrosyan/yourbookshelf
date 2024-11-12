from django.contrib import admin
from bookshelf.author.models import Author


# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass