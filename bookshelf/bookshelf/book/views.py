from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

from bookshelf.book.choices import BookStatusChoices
from bookshelf.book.forms import CreateBookForm
from bookshelf.book.models import Book, UserBookStatus


# Create your views here.


class CreateBookView(CreateView):
    template_name = 'book/add_book.html'
    model = Book
    form_class = CreateBookForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if not form.is_valid():
            print(form.errors)
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)


class BooksByGenreView(ListView):
    template_name = 'book/books_by_genre.html'
    context_object_name = 'books'

    def get_queryset(self):
        genre = self.kwargs['genre']
        return Book.objects.filter(genre=genre)


class BookDetailsView(DetailView):
    template_name = 'book/book_details.html'
    model = Book
    pk_url_kwarg = 'id'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book = self.get_object()

        current_status = None
        if self.request.user.is_authenticated:
            user_status = UserBookStatus.objects.filter(user=self.request.user, book=book).first()
            current_status = user_status.status if user_status else None

        context['status_choices'] = BookStatusChoices.choices
        context['current_status'] = current_status

        return context

