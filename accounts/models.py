from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PasswordHint(models.Model):
    username = models.CharField(max_length=200)
    hint = models.CharField(max_length=200, default="No hint available")

    def __str__(self):
        return self.name