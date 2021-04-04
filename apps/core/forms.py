from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .models import CoreUser


class CoreUserAddForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CoreUser
        fields = ('email','name',)

    def __init__(self, *args, **kwargs):
        '''Initialize with custom fields for Bootstrap'''
        super(CoreUserAddForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control',
                                                  'id': 'floatingEmail',
                                                  'placeholder': 'E-Mail'})
        self.fields['email'].widget.attrs.pop('autofocus', None)
        self.fields['email'].label = 'E-Mail'

        self.fields['name'].widget.attrs.update({'class':'form-control',
                                                 'id': 'floatingName',
                                                 'placeholder': 'Name'})
        self.fields['name'].label = 'Name'

        self.fields['password1'].widget.attrs.update({'class':'form-control',
                                                      'id': 'floatingPassword1',
                                                      'placeholder': 'Password'})
        self.fields['password1'].label = 'Password'

        self.fields['password2'].widget.attrs.update({'class':'form-control',
                                                      'id': 'floatingPassword2',
                                                      'placeholder': 'Confirm Password'})
        self.fields['password2'].label = 'Confirm Password'


class CoreUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CoreUser
        fields = ('email','name',)


class CoreAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CoreAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control w-100',
                                                     'id': 'floatingEmail',
                                                     'placeholder': 'E-Mail'})

        self.fields['password'].widget.attrs.update({'class': 'form-control w-100',
                                                      'id': 'floatingPassword',
                                                      'placeholder': 'Password',
                                                      'autocomplete': 'current-password'})
        self.error_messages.update({'invalid_login':
                                    _('Not a valid e-mail/password combination')})