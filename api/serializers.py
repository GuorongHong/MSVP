from rest_framework import serializers
from password import models

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'userid',
            'pw',
            'web',
        )
        model = models.Passwords