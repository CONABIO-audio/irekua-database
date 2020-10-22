from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from irekua_database import models


class UserInstitutionInline(admin.TabularInline):
    extra = 0

    model = models.UserInstitution

    verbose_name = _('Institution')

    verbose_name_plural = _('Institutions')

    autocomplete_fields = [
        'institution',
    ]


class UserCreationForm(forms.ModelForm):
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
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Passwords don't match"))

        return password2

    def save(self, commit=True):
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
            'is_active',
            'is_superuser',
            'is_curator',
            'is_model',
            'is_developer',
        )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_superuser',
        'is_curator',
        'is_model',
        'is_developer',
    )

    list_filter = (
        'userinstitution__institution',
        'is_superuser',
        'is_curator',
        'is_model',
        'is_developer',
    )

    fieldsets = (
        (None, {
            'fields': (
                'username',
                'password')
            }
         ),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_superuser',
                'is_curator',
                'is_model',
                'is_developer'
            )}
        ),
    )

    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )

    ordering = (
        'username',
    )

    filter_horizontal = ()

    inlines = [
        UserInstitutionInline,
    ]