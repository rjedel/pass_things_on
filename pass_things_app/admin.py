from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from pass_things_app.models import Institution, Donation

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Hasło (powtórz)', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Hasła do siebie nie pasują!')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


@admin.register(User)
class NewUserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = (
        'email', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined'
    )
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )

    filter_horizontal = ()


class DonationInline(admin.TabularInline):
    can_delete = False
    model = Donation


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    inlines = (DonationInline,)
    list_display = ('__str__', 'short_description', 'type', 'first_three_categories')

    @staticmethod
    def short_description(obj):
        return obj.description if len(obj.description) < 35 else (obj.description[:33] + '...')

    @staticmethod
    def first_three_categories(obj):
        return ', '.join(c.name for c in obj.categories.all()[:3])
