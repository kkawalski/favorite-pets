from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db import models


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    username = None
    email = models.EmailField(_('email address'), unique=True, blank=True)

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class Animal(models.Model):
    COLOR_RED = 'red'
    COLOR_BLUE = 'blue'
    COLOR_GREEN = 'green'
    COLOR_CHOICES = (
        (COLOR_RED, 'Red'),
        (COLOR_BLUE, 'Blue'),
        (COLOR_GREEN, 'Green'),
    )

    KIND_DOG = 1
    KIND_CAT = 2
    KIND_CHOICES = (
        (KIND_DOG, 'Dog'),
        (KIND_CAT, 'Cat'),
    )

    name = models.CharField(max_length=255)
    color = models.CharField(max_length=5, choices=COLOR_CHOICES)
    kind = models.SmallIntegerField(choices=KIND_CHOICES)
    owner = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,
        related_name='animals',
    )

    def __str__(self) -> str:
        return self.name
