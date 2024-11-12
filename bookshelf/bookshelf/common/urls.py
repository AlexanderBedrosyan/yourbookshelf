from django.urls import path
from .views import HomePageView, AddCommentView, EditCommentView, DeleteCommentView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add_comment/<int:book_id>/', AddCommentView.as_view(), name='add_comment'),
    path('edit_comment/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('delete_comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
]