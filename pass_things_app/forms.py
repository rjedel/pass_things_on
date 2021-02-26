from django import forms


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
