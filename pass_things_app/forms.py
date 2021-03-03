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
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.order_by('name'),
        widget=forms.CheckboxSelectMultiple,
    )
    bags = forms.IntegerField(
        min_value=1,
        max_value=32767,
        required=False,
        widget=forms.NumberInput(attrs={'step': '1'}),
    )
    organization = forms.ModelChoiceField(
        queryset=Institution.objects.order_by('name'),
        widget=forms.RadioSelect,
        empty_label=None,
    )
    address = forms.CharField(
        required=False,
    )
    city = forms.CharField(
        required=False,
    )
    postcode = forms.CharField(
        required=False,
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'type': 'phone'}),
    )
    data = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    more_info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '5'}),
    )
    more_info.widget.attrs.pop('cols', None)
