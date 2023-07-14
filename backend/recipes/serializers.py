import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, Tag, Ingredient, RecipeIngredient
from users.models import UserFollow
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):

    def convert_to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    color = serializers.CharField()
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    measurement_unit = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientRecipeSerializer(IngredientSerializer):
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        print(obj)
        print(self.data)
        return 1

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = IngredientRecipeSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    name = serializers.CharField()
    image = serializers.ImageField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorite',
            'is_in_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorite(self, value):
        # se
        # user = self.context['request'].user
        # if UserFollow.objects.get(author=author, user=user):
        #     return True
        return False

    def get_is_in_cart(self, value):
        return False
