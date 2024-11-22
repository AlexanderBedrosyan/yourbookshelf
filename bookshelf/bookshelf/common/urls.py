from django.urls import path
from .views import HomePageView, AddCommentView, EditCommentView, DeleteCommentView, FrontPageView, PermissionDeniedView, QuizGameView, SearchResultsView, CreateReportView

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('add_comment/<int:book_id>/', AddCommentView.as_view(), name='add_comment'),
    path('edit_comment/<int:pk>/', EditCommentView.as_view(), name='edit_comment'),
    path('delete_comment/<int:pk>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('', FrontPageView.as_view(), name='front-page'),
    path('permission_denied/', PermissionDeniedView.as_view(), name='permission-denied'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('report/', CreateReportView.as_view(), name='report'),
    path('quiz/', QuizGameView.as_view(), name='quiz')
]