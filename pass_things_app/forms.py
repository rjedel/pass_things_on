from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import validate_password

from .models import Category, Institution

User = get_user_model()


class RegisterForm(forms.Form):
    name = forms.CharField(label=False,
                           min_length=2,
                           max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': 'Imię'}))

    surname = forms.CharField(label=False,
                              min_length=2,
                              max_length=150,
                              widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))

    email = forms.EmailField(label=False,
                             max_length=254,
                             widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    password = forms.CharField(label=False,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
                               validators=[validate_password])

    password2 = forms.CharField(label=False,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}),
                                validators=[validate_password])

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Hasła do siebie nie pasują!')
        return cleaned_data


class CustomLoginForm(forms.Form):
    email = forms.EmailField(label=False, max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

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
        widget=forms.NumberInput(attrs={'step': '1'}),
    )
    organization = forms.ModelChoiceField(
        queryset=Institution.objects.order_by('name'),
        widget=forms.RadioSelect,
        empty_label=None,
    )
    address = forms.CharField()
    city = forms.CharField()
    postcode = forms.CharField()
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'phone'}),
    )
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )
    more_info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': '5'}),
    )
    more_info.widget.attrs.pop('cols', None)


class EditProfileForm(forms.ModelForm):
    email = forms.CharField(label=False,
                            max_length=254,
                            widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    first_name = forms.CharField(label=False,
                                 min_length=2,
                                 max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': 'Imię'}))

    last_name = forms.CharField(label=False,
                                min_length=2,
                                max_length=150,
                                widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))

    password = forms.CharField(label=False,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Obecne hasło', }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)

    # the email cannot be changed:
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = self.cleaned_data.get('password')
    #     email = self.cleaned_data.get('email')
    #     user = authenticate(email=email, password=password)
    #     if password and user is None:
    #         raise forms.ValidationError({'password': 'Błędne Hasło'})
    #     return cleaned_data


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=False,
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Stare hasło', }))
    new_password1 = forms.CharField(label=False,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło', }))
    new_password2 = forms.CharField(label=False,
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło (powtórz)', }))

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if old_password == new_password1 or old_password == new_password2:
            raise forms.ValidationError('Nowe hasło musi się różnić od starego')
        return cleaned_data
