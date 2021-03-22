from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _

from .models import CoreUser


class CoreUserAddForm(UserCreationForm):
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control'}),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = CoreUser
        fields = ('email','name',)


class CoreUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CoreUser
        fields = ('email',)


class CoreAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,
                                                           'class': 'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'form-control'}),
    )
