from django.shortcuts import render

# Create your views here.


def add_book(request):
    return render(request, 'book/add_book.html')