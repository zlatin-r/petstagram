from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from petstagram.accounts.managers import AppUserManager


class AppUser(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AppUserManager()

