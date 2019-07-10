from django.contrib import admin

# Register your models here.
from accounts.models import PasswordHint
admin.site.register(PasswordHint)