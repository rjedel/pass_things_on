from django.shortcuts import render
from django.views import View


class LandingPageView(View):
    def get(self, request):
        return render(request, 'pass_things_app/index.html')


class AddDonationView(View):
    def get(self, request):
        return render(request, 'pass_things_app/form.html')


class ConfirmationDonationView(View):
    def get(self, request):
        return render(request, 'pass_things_app/form-confirmation.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'pass_things_app/login.html')


class RegisterView(View):
    def get(self, request):
        return render(request, 'pass_things_app/register.html')
