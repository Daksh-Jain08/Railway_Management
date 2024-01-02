from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_customer = models.BooleanField('is_customer', default=False)
    is_staff = models.BooleanField('is_staff', default=False)
    money = models.IntegerField(default=0)

    def __str__(self):
        return self.username