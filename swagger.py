from rest_framework import serializers
from users.models import User


class SwaggerSignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class SwaggerSignupResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class SwaggerLoginRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
