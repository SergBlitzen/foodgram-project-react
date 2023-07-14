from rest_framework import serializers
from djoser.serializers import TokenCreateSerializer, SetPasswordSerializer

from .models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        read_only_fields = ('id',)


class CustomTokenCreateSerializer(TokenCreateSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, data):
        try:
            self.user = User.objects.get(email=data['email'], password=data['password'])
            return data
        except Exception:
            self.fail('invalid_credentials')


class CustomSetPasswordSerializer(SetPasswordSerializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_current_password(self, value):
        is_password_valid = (self.context["request"].user.password == value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = ('id',)

    def get_is_subscribed(self, value):
        return False
