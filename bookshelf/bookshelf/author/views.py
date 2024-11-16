from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from bookshelf.author.forms import UpdateAuthorForm, CreateAuthorForm
from bookshelf.author.models import Author


# Create your views here.


def add_author(request):
    return render(request, 'author/add_author.html')


class AuthorDetails(DetailView):
    template_name = 'author/author.html'
    model = Author
    pk_url_kwarg = 'author_id'


class EditAuthorView(LoginRequiredMixin, UpdateView):
    template_name = 'author/edit_author.html'
    pk_url_kwarg = 'author_id'
    model = Author
    form_class = UpdateAuthorForm

    def get_success_url(self):
        author_id = self.object.id
        return reverse_lazy('author-details', kwargs={'author_id': author_id})


class DeleteAuthorView(DeleteView):
    template_name = 'author/delete_author.html'
    model = Author
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy('home')


class CreateAuthorView(CreateView):
    form_class = CreateAuthorForm
    template_name = 'author/add_author.html'
    model = Author
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if not form.is_valid():
            print(form.errors)
            return self.form_invalid(form)

        form.instance.user = self.request.user
        return super().form_valid(form)