from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

class CoreUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError('The e-mail field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, date_joined=timezone.now(), **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        user_group = Group.objects.get(name='User')
        user.groups.add(user_group)
        
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        return self.create_user(email, password, **extra_fields)