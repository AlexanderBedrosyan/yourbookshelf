from django.urls import path, include
from . import views

urlpatterns = [
    path('add-author/', views.CreateAuthorView.as_view(), name='add-author'),
    path('authors/', views.ListAuthorsView.as_view(), name='authors'),
    path('<int:author_id>/', include([
        path('author-details/', views.AuthorDetails.as_view(), name='author-details'),
        path('edit-author/', views.EditAuthorView.as_view(), name='edit-author'),
        path('delete-author/', views.DeleteAuthorView.as_view(), name='delete-author'),
    ])),
]
