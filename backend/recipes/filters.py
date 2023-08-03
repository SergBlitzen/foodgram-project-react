import django_filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    """
    Фильтр для ингредиентов, который позволяет находить
    вхождения на странице создания рецептов.
    """

    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Основной фильтр для рецептов."""

    is_favorited = django_filters.NumberFilter(method='get_is_favorited')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__tag__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = django_filters.NumberFilter(method='get_cart')

    def get_cart(self, queryset, name, value):
        """Метод получения списка рецептов в корзине."""

        user = self.request.user
        # Все рецепты достаются из связанных с пользователем полей.
        if value:
            return queryset.filter(cart__user=user)
        else:
            return queryset

    def get_is_favorited(self, queryset, name, value):
        """Метод получения списка избранных рецептов."""

        user = self.request.user
        if value:
            return queryset.filter(recipefav__user=user)
        else:
            return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
