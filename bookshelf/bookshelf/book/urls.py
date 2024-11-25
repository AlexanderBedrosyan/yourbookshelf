from django.urls import path
from . import views

urlpatterns = [
    path('add-book/', views.CreateBookView.as_view(), name='add-book'),
    path('books-by-genre/<str:genre>/', views.BooksByGenreView.as_view(), name='books-by-genre'),
    path('<int:id>/book-details/', views.BookDetailsView.as_view(), name='book-details'),
    path('<int:id>/change_status/', views.UpdateBookStatusView.as_view(), name='book-status'),
    path('mybookshelf/<int:id>/', views.MyBookShelfView.as_view(), name='mybookshelf'),
]