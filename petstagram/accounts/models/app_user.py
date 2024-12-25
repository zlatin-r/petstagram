from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class AppUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # not really needed
