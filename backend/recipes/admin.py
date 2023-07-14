from django.contrib import admin

from .models import Recipe, Tag, Ingredient, Cart, RecipeTag, RecipeIngredient, RecipeFav


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
