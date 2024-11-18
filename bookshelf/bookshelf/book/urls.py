from django.urls import path
from . import views

urlpatterns = [
    path('add-book/', views.CreateBookView.as_view(), name='add-book'),
    path('books-by-genre/<str:genre>/', views.BooksByGenreView.as_view(), name='books-by-genre'),
    path('<int:id>/book-details/', views.BookDetailsView.as_view(), name='book-details'),
]