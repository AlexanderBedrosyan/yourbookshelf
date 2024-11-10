from django.urls import path
from . import views

urlpatterns = [
    path('add-author/', views.add_author, name='add-author')
]