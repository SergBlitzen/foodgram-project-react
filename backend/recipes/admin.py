from django.contrib import admin

from .models import Recipe, Tag, Ingredient, ShoppingCart, User, RecipeTag, RecipeIngredient, RecipeFav


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ingredients')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


