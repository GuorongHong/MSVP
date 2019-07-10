from django.contrib.auth import login

from rest_framework import generics
from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from password import models
from . import serializers

class ListPassword(generics.ListCreateAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = models.Passwords.objects.all()
    serializer_class = serializers.PasswordSerializer


class DetailPassword(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Passwords.objects.all()
    serializer_class = serializers.PasswordSerializer

# need to figure out how to decrypt password in API