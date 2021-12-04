import requests

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


class AnimalImage(models.Model):
    CATS_URL = 'https://dog.ceo/api/breeds/image/random'
    DOGS_URL = 'https://dog.ceo/api/breeds/image/random'

    KIND_DOG = 'cat'
    KIND_CAT = 'dog'
    KIND_CHOICES = (
        (KIND_DOG, 'Dog'),
        (KIND_CAT, 'Cat'),
    )

    ALLOWED_FILE_TYPES = ('png', 'gif', 'jpg', 'jpeg')
    FILE_TYPE_CHOICES = [(value, value.upper()) for value in ALLOWED_FILE_TYPES]

    url = models.TextField()
    kind = models.CharField(max_length=3, choices=KIND_CHOICES)
    file_type = models.CharField(max_length=4, choices=FILE_TYPE_CHOICES)
    user = models.ForeignKey(
        'core.User',
        on_delete=models.CASCADE,
        related_name='images'
    )

    @classmethod
    def get_animal_url(cls, kind):
        ANIMAL_URLS = {
            'cat': {'url': cls.CATS_URL, 'key': 'file'},
            'dog': {'url': cls.DOGS_URL, 'key': 'message'},
        }
        kind_api = ANIMAL_URLS.get(kind.lower())
        data = requests.get(kind_api['url']).json() or {}
        print(data)
        print(kind)
        url = data.get(kind_api['key'], '')
        print(url)
        file_type = url.split('.')[-1]
        print('URL', url)
        print(file_type)
        return url, file_type

    @classmethod
    def get_cat_image(cls, user):
        url, file_type = cls.get_animal_url('cat')
        return cls(url=url, file_type=file_type, user=user, kind='cat')
    
    @classmethod
    def get_dog_image(cls, user):
        url, file_type = cls.get_animal_url('dog')
        return cls(url=url, file_type=file_type, user=user, kind='dog')

    @classmethod
    def get_image(cls, kind, user):
        if kind.lower() == 'cat':
            return cls.get_cat_image(user)
        if kind.lower() == 'dog':
            return cls.get_dog_image(user)

    def __str__(self) -> str:
        return self.url.split('/')[-1]


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
