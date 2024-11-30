from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from bookshelf.accounts.models import CustomerModel
from bookshelf.author.models import Author
from bookshelf.book.choices import BookStatusChoices
from bookshelf.book.forms import CreateBookForm, UpdateBookForm
from bookshelf.book.models import Book, UserBookStatus
from bookshelf.book.serializers import BookSerializer
from bookshelf.mixins import PermissionCheckMixin
import asyncio


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


class UpdateBookStatusView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs.get('id'))
        status = request.POST.get('status')

        if request.user.is_authenticated:
            user_status, created = UserBookStatus.objects.get_or_create(user=request.user, book=book)
            user_status.status = status
            user_status.save()

        return redirect('home')


class MyBookShelfView(LoginRequiredMixin, DetailView):
    model = CustomerModel
    pk_url_kwarg = 'id'
    template_name = 'book/mybookshelf.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context['status_choices'] = BookStatusChoices.choices

        return context


class EditBookView(LoginRequiredMixin, PermissionCheckMixin, UpdateView):
    template_name = 'book/update_book.html'
    pk_url_kwarg = 'id'
    model = Book
    form_class = UpdateBookForm

    def get_success_url(self):
        return reverse_lazy('book-details', kwargs={'id': self.object.id})


class DeleteBookView(LoginRequiredMixin, PermissionCheckMixin, DeleteView):
    template_name = 'book/delete_book.html'
    model = Book
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')


class BookListApiView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

