from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from .models import Donation


class LandingPageView(View):
    def get(self, request):
        total_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        supported_institutions = Donation.objects.values('institution').distinct().count()
        ctx = {
            'total_quantity': total_quantity,
            'supported_institutions': supported_institutions,
        }
        return render(request, 'pass_things_app/index.html', context=ctx)


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
