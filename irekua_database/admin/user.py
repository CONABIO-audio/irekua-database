from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from irekua_database import models


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = (
            'username',
            'email',
            'institution')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = (
            'email',
            'password',
            'institution',
            'is_active',
            'is_superuser',
            'is_curator',
            'is_model',
            'is_developer')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username',
        'first_name',
        'last_name',
        'institution',
        'is_superuser',
        'is_curator',
        'is_model',
        'is_developer',
    )
    list_filter = (
        'institution',
        'is_superuser',
        'is_curator',
        'is_model',
        'is_developer',
    )
    fieldsets = (
        (None, {'fields': (
            'username',
            'password')}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'institution')}),
        (_('Permissions'), {'fields': (
            'is_superuser',
            'is_curator',
            'is_model',
            'is_developer'
        )}),
    )
    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
        'institution__institution_name')
    ordering = ('username', )
    filter_horizontal = ()
