from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('logout-confirmation/', views.logout, name='logout-page'),
    path('logout/', views.CustomerLogoutView.as_view(), name='logout'),
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('<int:id>/details/', views.CustomerDetailsView.as_view(), name='account-details'),
    path('<int:id>/edit/', views.EditAccountView.as_view(), name='edit-account'),
]