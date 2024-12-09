from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView
from bookshelf.author.forms import UpdateAuthorForm, CreateAuthorForm
from bookshelf.author.models import Author
from ..common.forms import CreateReportForm
from ..common.models import Report
from ..mixins import PermissionCheckMixin
from asgiref.sync import sync_to_async


# Create your views here.


def add_author(request):
    return render(request, 'author/add_author.html')


class AuthorDetails(DetailView):
    template_name = 'author/author.html'
    model = Author
    pk_url_kwarg = 'author_id'


class EditAuthorView(LoginRequiredMixin, PermissionCheckMixin, UpdateView):
    template_name = 'author/edit_author.html'
    pk_url_kwarg = 'author_id'
    model = Author
    form_class = UpdateAuthorForm

    def get_success_url(self):
        author_id = self.object.id
        return reverse_lazy('author-details', kwargs={'author_id': author_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.date_of_birth:
            context['date_of_birth'] = self.object.date_of_birth.strftime('%Y-%m-%d')
        return context

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class DeleteAuthorView(LoginRequiredMixin, PermissionCheckMixin, DeleteView):
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


class ListAuthorsView(ListView):
    model = Author
    template_name = 'author/authors.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return Author.objects.order_by('first_name')


class AuthorListView(View):
    async def get(self, request, *args, **kwargs):
        authors = await sync_to_async(self.get_authors)()

        data = await sync_to_async(self.format_authors)(authors)

        return render(request, 'author/book_per_author.html', {'authors': data})

    def get_authors(self):
        return Author.objects.filter(approved=True)

    def format_authors(self, authors):
        return [
            {
                'name': f'{author.first_name} {author.last_name}',
                'books': [{'title': book.title, 'description': book.description} for book in author.books.filter(approved=True)]
            }
            for author in authors
        ]