from rest_framework import generics

from password import models
from . import serializers

class ListPassword(generics.ListCreateAPIView):
    queryset = models.Passwords.objects.all()
    serializer_class = serializers.PasswordSerializer


class DetailPassword(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Passwords.objects.all()
    serializer_class = serializers.PasswordSerializer

# need to figure out how to decrypt password in API