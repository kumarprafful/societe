from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Provide your email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be a staff.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be a superman.')
        return self._create_user(email, password, **kwargs)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
