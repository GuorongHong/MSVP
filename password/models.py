from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userid = models.CharField(max_length = 200)
    pw = models.CharField(max_length = 200)
    web = models.CharField(max_length = 200)
    def __str__(self):
        return self.web

class MasterHint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hint = models.CharField(max_length = 200, null=True)
    def __str__(self):
        return self.web