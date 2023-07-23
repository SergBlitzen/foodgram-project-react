from rest_framework import serializers
from djoser.serializers import TokenCreateSerializer, SetPasswordSerializer

from recipes.models import Recipe
from .models import User, UserFollow


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

    def get_is_subscribed(self, obj):
        try:
            user = self.context['request'].user
        # Перехват ошибки для метода update.
        except Exception:
            user = obj
        author = obj
        try:
            follow = UserFollow.objects.get(user=user, author=author)
            if follow:
                return True
        except Exception:
            return False


class UserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserFollowSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return UserRecipeSerializer(recipes, many=True, context=self.context).data

    def get_recipes_count(self, obj):
        recipes_count = Recipe.objects.filter(author=obj).count()
        return recipes_count

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
