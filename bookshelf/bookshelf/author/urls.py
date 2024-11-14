from django.urls import path
from . import views

urlpatterns = [
    path('add-author/', views.add_author, name='add-author'),
    path('<int:author_id>/author-details/', views.AuthorDetails.as_view(), name='author-details'),
    path('<int:author_id>/edit-author/', views.EditAuthorView.as_view(), name='edit-author'),
]