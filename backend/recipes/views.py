from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserRecipeSerializer
from .models import Recipe, Tag, Ingredient, RecipeFav, Cart
from .serializers import RecipeSerializer, TagSerializer, \
    IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=True, url_path='favorite', methods=['post'])
    def favorite(self, request, pk=None):
        instance = self.get_object()
        if RecipeFav.objects.filter(recipe=instance, user=self.request.user):
            return Response({"error": "Рецепт уже находится в избранном."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            RecipeFav.objects.create(recipe=instance, user=self.request.user)
            context = self.get_renderer_context()
            serializer = UserRecipeSerializer(instance, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        instance = self.get_object()
        if obj := RecipeFav.objects.filter(recipe=instance, user=self.request.user):
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Рецепт не находится в избранном."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, url_path='shopping_cart', methods=['post'])
    def favorite(self, request, pk=None):
        instance = self.get_object()
        if Cart.objects.filter(recipe=instance, user=self.request.user):
            return Response({"error": "Рецепт уже находится в корзине."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            Cart.objects.create(recipe=instance, user=self.request.user)
            context = self.get_renderer_context()
            serializer = UserRecipeSerializer(instance, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        instance = self.get_object()
        if obj := Cart.objects.filter(recipe=instance, user=self.request.user):
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Рецепт не находится в корзине."}, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
