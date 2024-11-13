from django.shortcuts import render
from django.views.generic import DetailView

from bookshelf.author.models import Author


# Create your views here.


def add_author(request):
    return render(request, 'author/add_author.html')


class AuthorDetails(DetailView):
    template_name = 'author/author.html'
    model = Author
    pk_url_kwarg = 'author_id'