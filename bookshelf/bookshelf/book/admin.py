from django.contrib import admin

from bookshelf.book.models import Book, UserBookStatus


# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(UserBookStatus)
class BookAdmin(admin.ModelAdmin):
    pass