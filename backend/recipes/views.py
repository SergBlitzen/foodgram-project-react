from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserRecipeSerializer
from .filters import IngredientFilter, RecipeFilter
from .models import Recipe, Tag, Ingredient, RecipeFav, Cart, RecipeIngredient
from .serializers import RecipeSerializer, TagSerializer, \
    IngredientSerializer
from .utils import create_instance, delete_instance


class RecipeViewSet(viewsets.ModelViewSet):
    """Viewset для эндпоинта 'recipes/'"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter

    http_method_names = ['get', 'post', 'patch', 'delete']

    # Взаимодействие с отдельными объектами рецептов реализовано
    # в action-функциях с кастомными функциями для создания
    # и удаления элементов.
    @action(methods=['post'], detail=True, url_path='favorite',
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Action-функция для создания элемента избранного рецепта."""

        model = RecipeFav
        serializer = UserRecipeSerializer
        context = self.get_serializer_context()
        message = {"error": "Рецепт уже находится в избранном."}
        instance = 'recipe'
        objects = {
            'recipe': self.get_object(),
            'user': self.request.user
        }
        return create_instance(model, serializer, context, message, instance, objects)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        """Action-функция для удаления элемента избранного рецепта."""

        model = RecipeFav
        message = {"error": "Рецепт не находится в избранном."}
        objects = {
            'recipe': self.get_object(),
            'user': self.request.user
        }

        return delete_instance(model, message, objects)

    @action(methods=['post'], detail=True, url_path='shopping_cart',
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Action-функция для создания элемента рецепта в корзине."""

        model = Cart
        serializer = UserRecipeSerializer
        context = self.get_serializer_context()
        message = {"error": "Рецепт уже находится в корзине."}
        instance = 'recipe'
        objects = {
            'recipe': self.get_object(),
            'user': self.request.user
        }

        return create_instance(model, serializer, context, message, instance, objects)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        """Action-функция для удаления элемента рецепта в корзине."""

        model = Cart
        message = {"error": "Рецепт не находится в корзине."}
        objects = {
            'recipe': self.get_object(),
            'user': self.request.user
        }

        return delete_instance(model, message, objects)

    @action(detail=False, url_path='download_shopping_cart',
            methods=['get'], permission_classes=[IsAuthenticated])
    def download_cart(self, request):
        """
        Возвращает .txt-файл со списком всех добавленных в корзину
        рецептов и ингредиентов для них.
        """

        recipes_data = []
        recipes = [obj.recipe for obj in Cart.objects.filter(user=request.user)]
        for recipe in recipes:
            recipe_ingredients = f'{recipe.name}: \n'
            for obj in RecipeIngredient.objects.filter(recipe=recipe):
                recipe_ingredients += str(obj.ingredient.name) + ' '
                recipe_ingredients += str(obj.amount) + ' '
                recipe_ingredients += str(obj.ingredient.measurement_unit) + '\n'
            recipes_data.append(recipe_ingredients)
        response = HttpResponse(recipes_data, content_type='txt')
        response['Content-Disposition'] = 'attachment; filename="shopping_list"'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для эндпоинта 'tags/'"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    filterset_fields = ['slug', ]


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset для эндпоинта 'ingredients/'"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filterset_class = IngredientFilter
