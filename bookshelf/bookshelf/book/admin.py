from django.contrib import admin
from bookshelf.book.models import Book, UserBookStatus

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'approved', 'average_rating')
    search_fields = ('title', 'author__name', 'genre')
    list_filter = ('genre', 'approved', 'author')
    list_editable = ('approved',)
    fields = ('title', 'author', 'genre', 'description', 'picture_url', 'approved')
    actions = ['mark_as_approved']

    def mark_as_approved(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, "Selected books have been marked as approved.")

    mark_as_approved.short_description = "Mark selected books as approved"


@admin.register(UserBookStatus)
class BookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status')
    search_fields = ('user__username', 'book__title', 'status')
    list_filter = ('status', 'book__genre')
    fields = ('user', 'book', 'status')
    readonly_fields = ('user', 'book', 'status')

