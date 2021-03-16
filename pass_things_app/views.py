import json

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import RegisterForm, CustomLoginForm, AddDonationForm, EditProfileForm, UserPasswordChangeForm
from .models import Donation, Institution

User = get_user_model()


class LandingPageView(View):
    def get(self, request):
        total_quantity = Donation.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
        supported_institutions = Donation.objects.values('institution').distinct().count()

        ctx = {
            'total_quantity': total_quantity,
            'supported_institutions': supported_institutions,
        }

        return render(request, 'pass_things_app/index.html', context=ctx)


class InstitutionsView(View):
    def get(self, request):
        if request.is_ajax():
            foundations = Institution.objects.filter(type=Institution.FOUNDATION).order_by('name')
            foundations = [(f.name, f.description, ', '.join(c.name for c in f.categories.all())) for f in foundations]

            ngos = Institution.objects.filter(type=Institution.NGO).order_by('name')
            ngos = [(f.name, f.description, ', '.join(c.name for c in f.categories.all())) for f in ngos]

            local_donations = Institution.objects.filter(type=Institution.LOCAL_DONATION).order_by('name')
            local_donations = [(f.name, f.description, ', '.join(c.name for c in f.categories.all())) for f in
                               local_donations]

            return JsonResponse({
                'foundations': foundations,
                'ngos': ngos,
                'local_donations': local_donations,
            })

        return JsonResponse({})


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
        form = CustomLoginForm(auto_id=False, )
        ctx = {
            'form': form,
        }
        return render(request, 'pass_things_app/login.html', context=ctx)

    def post(self, request):
        form = CustomLoginForm(data=request.POST, auto_id=False, )
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
        form = RegisterForm(auto_id=False, )
        ctx = {
            'form': form,
        }
        return render(request, 'pass_things_app/register.html', context=ctx)

    def post(self, request):
        form = RegisterForm(data=request.POST, auto_id=False)
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


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_donations = Donation.objects.filter(user=user).order_by('-pick_up_date', '-pick_up_time')
        ctx = {
            'user': user,
            'user_donations': user_donations,
        }
        return render(request, 'pass_things_app/profile.html', context=ctx)

    def post(self, request):
        if request.is_ajax():
            donation_pk = request.POST.get('donationPk')
            donation_val = request.POST.get('donationVal')

            if donation_pk and donation_val:
                user_donations = get_object_or_404(Donation, user=request.user, pk=donation_pk)

                if donation_val == 'yes':
                    user_donations.is_taken = True
                elif donation_val == 'no':
                    user_donations.is_taken = False
                elif donation_val == 'unknown':
                    user_donations.is_taken = None

                user_donations.save()
                return JsonResponse({'response': True})
            return JsonResponse({'response': False})

        return JsonResponse({})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user, auto_id=False)
        return render(request, 'pass_things_app/edit_profile.html', {'form': form})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user, auto_id=False)
        # password = form.data['password']
        # if password and not request.user.check_password(password):
        #     form.add_error('password', 'Błędne Hasło')
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
        return render(request, 'pass_things_app/edit_profile.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserPasswordChangeForm(user=request.user)
        return render(request, 'pass_things_app/change_password.html', {'form': form})

    def post(self, request):
        form = UserPasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            ctx = {'msg': 'Hasło zmienione poprawnie', }
            return render(request, 'pass_things_app/change_password.html', context=ctx)

        return render(request, 'pass_things_app/change_password.html', {'form': form})
