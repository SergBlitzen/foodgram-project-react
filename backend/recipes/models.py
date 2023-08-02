from django.core.validators import MinValueValidator
from django.db import models

from colorfield.fields import ColorField

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name='Название тега',
        help_text='Введите название тега'
    )
    color = ColorField(
        max_length=7,
        unique=True,
        null=False,
        verbose_name='Цвет тега',
        help_text='Введите цвет тега в HEX-кодировке'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=False,
        verbose_name='Slug тега',
        help_text='Введите slug тега'
    )

    class Meta:
        verbose_name = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        null=False,
        unique=True,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10,
        null=False,
        verbose_name='Мера объёма ингредиента',
        help_text='Введите меру измерения ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта'
    )
    image = models.ImageField(
        null=False,
        upload_to='recipes/images',
        verbose_name='Изображение рецепта',
        help_text='Выберите изображение рецепта'
    )
    name = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта'
    )
    text = models.TextField(
        null=False,
        verbose_name='Способ приготовления',
        help_text='Опишите способ приготовления'
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        verbose_name='Время готовки',
        help_text='Укажите время готовки в минутах'
    )
    publish_date = models.DateTimeField(
        verbose_name='Дата публикации рецепта',
        auto_now_add=True
    )
    # У рецептов отсутствуют поля тегов и ингредиентов, но связь с ними
    # налажена благодаря связанным таблицам. Это несколько снижает явность
    # кода (и не уверен, насколько снижает оптимизацию), но с такой
    # архитектурой сериализация становится на несколько порядков проще.

    class Meta:
        verbose_name = 'Рецепты'
        ordering = ('-publish_date',)

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='tags',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт для тега'
    )
    tag = models.ForeignKey(
        Tag,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Тег',
        help_text='Укажите тег для рецепта'
    )

    class Meta:
        verbose_name = 'Теги рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipe_tag'
            )
        ]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт для ингредиента'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        help_text='Укажите ингредиент для рецепта'
    )
    amount = models.PositiveIntegerField(
        null=False,
        verbose_name='Количество ингредиентов',
        help_text='Укажите количество ингредиента',
        validators=[MinValueValidator(
            1, message="Количество ингредиентов должно быть больше нуля!")]
    )

    class Meta:
        verbose_name = 'Ингредиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient', 'amount'),
                name='unique_recipe_ingredient_amount'
            )
        ]


class RecipeFav(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя для избранного рецепта'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт для добавление в избранное'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe'
            )
        ]


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        help_text='Укажите рецепт для добавления в корзину'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя для рецепта в корзине'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_user'
            )
        ]
