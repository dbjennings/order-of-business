from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

class CoreUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('The given e-mail must be set')
        email = self.normalize_email(email)
        
        user = self.model(email=email, is_active=True, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user