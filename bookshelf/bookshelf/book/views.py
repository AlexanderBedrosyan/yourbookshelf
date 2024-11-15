from django.shortcuts import render
from django.views.generic import DetailView, ListView

from bookshelf.book.models import Book


# Create your views here.


def add_book(request):
    return render(request, 'book/add_book.html')


def books_by_genre(request):
    return render(request, 'book/books_by_genre.html')


class BooksByGenreView(ListView):
    template_name = 'book/books_by_genre.html'
    context_object_name = 'books'

    def get_queryset(self):
        genre = self.kwargs['genre']
        return Book.objects.filter(genre=genre)