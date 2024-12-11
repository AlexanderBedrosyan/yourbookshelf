from django.urls import path, include
from .views import (HomePageView, AddCommentView, EditCommentView, DeleteCommentView, FrontPageView, PermissionDeniedView,
                    QuizGameView, SearchResultsView, CreateReportView, SubmitAnswerView, NextQuestionView, AddRatingView,
                    ReportsView, SingleReportView, AllCommentsForSingleBookView)

urlpatterns = [
    path('home/', HomePageView.as_view(), name='home'),
    path('<int:pk>/', include([
        path('add_comment/', AddCommentView.as_view(), name='add_comment'),
        path('edit_comment/', EditCommentView.as_view(), name='edit_comment'),
        path('delete_comment/', DeleteCommentView.as_view(), name='delete_comment'),
        ])),
    path('', FrontPageView.as_view(), name='front-page'),
    path('permission_denied/', PermissionDeniedView.as_view(), name='permission-denied'),
    path('search/', SearchResultsView.as_view(), name='search-results'),
    path('report/', CreateReportView.as_view(), name='report'),
    path('quiz/', QuizGameView.as_view(), name='quiz'),
    path('quiz/submit_answer/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('quiz/next_question/', NextQuestionView.as_view(), name='next-question'),
    path('rate_book/<int:book_id>/', AddRatingView.as_view(), name='rate-book'),
    path('all_reports/', ReportsView.as_view(), name='reports'),
    path('<int:id>/single_report/', SingleReportView.as_view(), name='single-report'),
    path('<int:id>/book-comments', AllCommentsForSingleBookView.as_view(), name='all-comments')
]