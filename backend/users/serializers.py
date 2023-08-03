from recipes.models import Recipe
from rest_framework import serializers

from .models import User, UserFollow


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    password = serializers.CharField()

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

    def create(self, validated_data):
        """Метод для POST-запроса."""

        password = validated_data.pop('password')
        user = super().create(validated_data)
        # Отдельная установка пароля для того, чтобы он захешировался.
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Основнйо сериализатор для вывода информации о пользователе."""
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
        """Метод получения статуса подписки на пользователя."""

        try:
            user = self.context['request'].user
        # Перехват ошибки для метода update, в который передаётся
        # объект самого пользователя.
        except Exception:
            user = obj
        author = obj
        if UserFollow.objects.filter(user=user, author=author):
            return True
        else:
            return False


class UserRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи рецептов в сериализаторе пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserFollowSerializer(UserSerializer):
    """
    Сериалиатор для получения информации о пользователе
    в зоне подписок.
    """

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        """Метод получения рецептов пользователя."""

        recipes = Recipe.objects.filter(author=obj)
        return UserRecipeSerializer(
            recipes, many=True, context=self.context
        ).data

    def get_recipes_count(self, obj):
        """Метод получения количества рецептов пользователя."""

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
