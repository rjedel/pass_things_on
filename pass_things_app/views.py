from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from .models import Donation, Institution


class LandingPageView(View):
    def get(self, request):
        total_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum']
        supported_institutions = Donation.objects.values('institution').distinct().count()

        foundations = Institution.objects.filter(type=Institution.TYPE_CHOICES[0][0]).order_by('?')[:3]
        for foundation in foundations:
            foundation.categories_str = ', '.join(cat.name for cat in foundation.categories.order_by('name')[:5])

        ngos = Institution.objects.filter(type=Institution.TYPE_CHOICES[1][0]).order_by('?')[:4]
        for ngo in ngos:
            ngo.categories_str = ', '.join(cat.name for cat in ngo.categories.order_by('name')[:5])

        local_donations = Institution.objects.filter(type=Institution.TYPE_CHOICES[2][0]).order_by('?')[:2]
        for ld in local_donations:
            ld.categories_str = ', '.join(cat.name for cat in ld.categories.order_by('name')[:5])

        ctx = {
            'total_quantity': total_quantity,
            'supported_institutions': supported_institutions,
            'foundations': foundations,
            'ngos': ngos,
            'local_donations': local_donations,
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
