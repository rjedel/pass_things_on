from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import RegisterForm, CustomLoginForm
from .models import Donation, Institution, Category

User = get_user_model()


class LandingPageView(View):
    def get(self, request):
        total_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        supported_institutions = Donation.objects.values('institution').distinct().count()

        foundations = Institution.objects.filter(type=Institution.FOUNDATION).order_by('?')[:3]
        ngos = Institution.objects.filter(type=Institution.NGO).order_by('?')[:4]
        local_donations = Institution.objects.filter(type=Institution.LOCAL_DONATION).order_by('?')[:2]

        ctx = {
            'total_quantity': total_quantity,
            'supported_institutions': supported_institutions,
            'foundations': foundations,
            'ngos': ngos,
            'local_donations': local_donations,
        }
        return render(request, 'pass_things_app/index.html', context=ctx)


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.order_by('name')
        institutions = Institution.objects.order_by('name')
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'pass_things_app/form.html', context=ctx)


class FilterInstitutionsView(View):
    def get(self, request):
        if request.is_ajax():
            data = request.GET.get('categories_ids')
            if data:
                categories_lst = [int(i) for i in list(data.replace(',', ''))]
                filtered_institutions = Institution.objects.filter(categories__in=categories_lst)
                filtered_institutions = list(filtered_institutions.distinct().values_list('id', flat=True))
                return JsonResponse({'filtered_ins': filtered_institutions})
            return JsonResponse({'filtered_ins': ''})

        return JsonResponse({})


class ConfirmationDonationView(View):
    def get(self, request):
        return render(request, 'pass_things_app/form-confirmation.html')


class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('landing_page'))
        form = CustomLoginForm()
        ctx = {
            'form': form,
        }
        return render(request, 'pass_things_app/login.html', context=ctx)

    def post(self, request):
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect(request.GET.get('next', settings.LOGIN_REDIRECT_URL))
        return render(request, 'pass_things_app/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('landing_page'))
        form = RegisterForm()
        ctx = {
            'form': form,
        }
        return render(request, 'pass_things_app/register.html', context=ctx)

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['name']
            last_name = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            return redirect(reverse('login'))
        return render(request, 'pass_things_app/register.html', {'form': form})
