from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from bookshelf.book.forms import UpdateCommentForm, DeleteCommentForm
from bookshelf.book.models import Book, Rating, Comment


# Create your views here.


class HomePageView(ListView):
    template_name = 'common/home.html'
    model = Book
    context_object_name = 'books'


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        book_id = kwargs.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        text = request.POST.get("text")

        if text:
            Comment.objects.create(user=request.user, book=book, text=text)

        return redirect(reverse_lazy('home'))


class EditCommentView(LoginRequiredMixin, UpdateView):
    template_name = 'book/edit_comment.html'
    pk_url_kwarg = 'pk'
    model = Comment
    form_class = UpdateCommentForm
    success_url = reverse_lazy('home')


class DeleteCommentView(DeleteView):
    pk_url_kwarg = 'pk'
    template_name = 'book/delete_comment.html'
    success_url = reverse_lazy('home')
    form_class = DeleteCommentForm
    model = Comment

    def get_initial(self):
        return self.object.__dict__

    def form_invalid(self, form):
        return self.form_valid(form)



