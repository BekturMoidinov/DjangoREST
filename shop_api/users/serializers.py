from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserRegistrationValidationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError("This username already exists.")

class UserAuthenticationValidationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CodeValidationSerializer(serializers.Serializer):
    code = serializers.IntegerField(min_value=6)
