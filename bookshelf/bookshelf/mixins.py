from django.db.models import F, CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.contrib import messages

from bookshelf.author.models import Author
from bookshelf.book.models import Book


class PermissionCheckMixin:
    DENIED_MESSAGE = "Access denied. You do not have the required permissions to view this page."

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (obj.user == request.user or request.user.is_superuser or request.user.is_staff):
            messages.error(request, self.DENIED_MESSAGE)
            return redirect('permission-denied')
        return super().get(request, *args, **kwargs)


class PermissionOnlyForStaffs:
    DENIED_MESSAGE = "Access denied. You do not have the required permissions to view this page."

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, self.DENIED_MESSAGE)
            return redirect('permission-denied')
        return super().get(request, *args, **kwargs)


class MinUniqueAuthors:
    MIN_NEEDED_AUTHORS = 3

    def get(self, request, *args, **kwargs):
        unique_authors = list(Author.objects.annotate(
            full_name=Concat(
                F('first_name'),
                Value(' '),
                F('last_name'),
                output_field=CharField()
            )
        ).values_list('full_name', flat=True).distinct())

        if len(unique_authors) < self.MIN_NEEDED_AUTHORS:
            messages.error(request, 'The quiz is still on progress!')
            return redirect('permission-denied')

        return super().get(request, *args, **kwargs)


class MinBooksNeeded:
    MIN_BOOKS_NEEDED = 2

    def get(self, request, *args, **kwargs):
        books = Book.objects.filter(approved=True)

        if len(books) < self.MIN_BOOKS_NEEDED:
            messages.error(request, 'The quiz is still on progress!')
            return redirect('permission-denied')

        return super().get(request, *args, **kwargs)
