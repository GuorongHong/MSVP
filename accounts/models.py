from django.db import models
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your models here.
class CustomManager(models.Manager):
    def get_or_create(self, **kwargs):
        defaults = kwargs.pop('defaults', {})  # popping defaults from values
        for key, value in kwargs.items():
            if value == None:
                kwargs[key] = defaults.get(key)
        return super(CustomManager, self).get_or_create(**kwargs)

class PasswordHint(models.Model):
    username = models.CharField(max_length=200)
    hint = models.CharField(max_length=200)

    objects = CustomManager()