from django.contrib import admin

from .models import Recipe, Tag, Ingredient,\
    Cart, RecipeTag, RecipeIngredient, RecipeFav


class TagInLine(admin.StackedInline):
    """Вложенная панель с тегами для модели рецептов."""
    model = RecipeTag
    extra = 1


class IngredientInline(admin.StackedInline):
    """Вложенная модель с ингредиентами для модели рецептов."""
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, TagInLine]
    list_display = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


@admin.register(RecipeFav)
class RecipeFavAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')
