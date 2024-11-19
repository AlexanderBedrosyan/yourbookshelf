from django import template
from bookshelf.book.models import Book

register = template.Library()


@register.simple_tag
def get_unique_genres():
    return Book.objects.values('genre').distinct()