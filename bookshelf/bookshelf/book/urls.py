from django.urls import path
from . import views

urlpatterns = [
    path('add-book/', views.add_book, name='add-book'),
    path('books-by-genre/<str:genre>/', views.BooksByGenreView.as_view(), name='books-by-genre'),
]