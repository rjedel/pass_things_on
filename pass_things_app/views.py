import json

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import RegisterForm, CustomLoginForm, AddDonationForm
from .models import Donation, Institution

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
        form = AddDonationForm(auto_id=False)
        ctx = {
            'form': form,
        }
        return render(request, 'pass_things_app/form.html', context=ctx)

    def post(self, request):
        if request.is_ajax():
            form = AddDonationForm(request.POST)

            if form.is_valid():
                form_inputs = {
                    'quantity': form.cleaned_data['bags'],
                    'institution': form.cleaned_data['organization'],
                    'address': form.cleaned_data['address'],
                    'phone_number': form.cleaned_data['phone'],
                    'city': form.cleaned_data['city'],
                    'zip_code': form.cleaned_data['postcode'],
                    'pick_up_date': form.cleaned_data['data'],
                    'pick_up_time': form.cleaned_data['time'],
                    'pick_up_comment': form.cleaned_data['more_info'],
                    'user': request.user,
                }
                d = Donation(**form_inputs)
                d.save()
                d.categories.set(form.cleaned_data['categories'])
                return JsonResponse({'response': True})
            return JsonResponse({'response': False})

        return JsonResponse({})


class FilterInstitutionsView(View):
    def get(self, request):
        if request.is_ajax():
            categories_lst = json.loads(request.GET.get('categories_ids'))
            if categories_lst:
                filtered_institutions = Institution.objects.all()
                for pk in categories_lst:
                    filtered_institutions = filtered_institutions.filter(categories__id=pk)
                filtered_institutions = list(
                    filtered_institutions.distinct().values_list('id', 'name', 'description', )
                )
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
