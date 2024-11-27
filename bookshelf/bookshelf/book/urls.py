from django.urls import path, include
from . import views

urlpatterns = [
    path('add-book/', views.CreateBookView.as_view(), name='add-book'),
    path('books-by-genre/<str:genre>/', views.BooksByGenreView.as_view(), name='books-by-genre'),
    path('<int:id>/', include([
         path('book-details/', views.BookDetailsView.as_view(), name='book-details'),
         path('change_status/', views.UpdateBookStatusView.as_view(), name='book-status'),
         path('edit_book/', views.EditBookView.as_view(), name='edit-book'),
         path('delete_book/', views.DeleteBookView.as_view(), name='delete-book'),
        ])),
    path('mybookshelf/<int:id>/', views.MyBookShelfView.as_view(), name='mybookshelf'),
]