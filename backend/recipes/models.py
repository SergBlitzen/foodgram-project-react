from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    color = models.CharField(max_length=7, unique=True, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    measurement_unit = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, related_name='recipe', on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=False, upload_to='recipes/images')
    name = models.CharField(max_length=200, blank=False, null=False)
    text = models.TextField(blank=False, null=False)
    cooking_time = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Cart(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user'
            )
        ]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipe_tag'
            )
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient', 'amount'),
                name='unique_recipe_ingredient_amount'
            )
        ]


class RecipeFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe'
            )
        ]

