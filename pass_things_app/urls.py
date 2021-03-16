from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('add_donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('filter_institutions/', views.FilterInstitutionsView.as_view(), name='filter_institutions'),
    path('institutions/', views.InstitutionsView.as_view(), name='institutions'),
    path('confirmation_donation/', views.ConfirmationDonationView.as_view(), name='confirmation_donation'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
]
