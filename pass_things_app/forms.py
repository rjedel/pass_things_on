from django import forms
from django.contrib.auth import authenticate

from .models import Category, Institution


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Hasła do siebie nie pasują!')
        return cleaned_data


class CustomLoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError('Niepoprawny e-mail i / lub hasło')
        return cleaned_data


class AddDonationForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.order_by('name'), )
    bags = forms.IntegerField(
        min_value=1,
        max_value=32767,
        required=False,
        widget=forms.NumberInput(attrs={'step': '1'}),
    )
    institutions = forms.ModelChoiceField(queryset=Institution.objects.order_by('name'), empty_label=None, )
