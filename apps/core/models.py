from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CoreUserManager

class CoreUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CoreUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
