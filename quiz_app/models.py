from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(null=True, max_length=50)
    email = models.CharField(max_length=20)
    carrier = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=5, null=True, blank=True)