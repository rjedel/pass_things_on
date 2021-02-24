from django.urls import path

from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('confirmation_donation/', views.ConfirmationDonationView.as_view(), name='confirmation_donation'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
