import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Recipe, Tag, Ingredient, RecipeIngredient, RecipeTag, RecipeFav, Cart
from users.serializers import UserSerializer, UserRecipeSerializer


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.pk')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeTagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='tag.pk')
    name = serializers.CharField(source='tag.name')
    color = serializers.CharField(source='tag.color')
    slug = serializers.CharField(source='tag.slug')

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    author = UserSerializer(default=serializers.CurrentUserDefault())
    ingredients = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    name = serializers.CharField()
    image = Base64ImageField(use_url=True)
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

    def get_ingredients(self, obj):
        ingredients = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_tags(self, obj):
        tags = RecipeTag.objects.filter(recipe=obj)
        return RecipeTagSerializer(tags, many=True).data

    def get_is_favorite(self, obj):
        try:
            user = self.context['request'].user
            if RecipeFav.objects.get(recipe=obj, user=user):
                return True
        except Exception:
            return False

    def get_is_in_cart(self, obj):
        try:
            user = self.context['request'].user
            if Cart.objects.get(recipe=obj, user=user):
                return True
        except Exception:
            return False

    def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data)
        for tag_id in self.initial_data['tags']:
            tag = Tag.objects.get(pk=tag_id)
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        for ingredient_data in self.initial_data['ingredients']:
            ingredient = Ingredient.objects.get(pk=ingredient_data['id'])
            amount = ingredient_data['amount']
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
        return recipe

    def update(self, instance, validated_data):
        RecipeTag.objects.filter(recipe=instance).delete()
        for tag_id in self.initial_data['tags']:
            tag = Tag.objects.get(pk=tag_id)
            RecipeTag.objects.create(recipe=instance, tag=tag)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient_data in self.initial_data['ingredients']:
            ingredient = Ingredient.objects.get(pk=ingredient_data['id'])
            amount = ingredient_data['amount']
            RecipeIngredient.objects.create(recipe=instance, ingredient=ingredient, amount=amount)
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.image = validated_data['image']
        instance.cooking_time = validated_data['cooking_time']
        instance.save()
        return instance
