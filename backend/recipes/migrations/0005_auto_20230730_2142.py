# Generated by Django 3.2.3 on 2023-07-30 18:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0004_auto_20230730_1943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ингредиенты рецептов'},
        ),
        migrations.AlterModelOptions(
            name='recipetag',
            options={'verbose_name': 'Теги рецептов'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Теги'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='recipe',
            field=models.ForeignKey(help_text='Укажите рецепт для добавления в корзину', on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(help_text='Укажите пользователя для рецепта в корзине', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(help_text='Введите меру измерения ингредиента', max_length=200, verbose_name='Мера объёма ингредиента'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(help_text='Введите название ингредиента', max_length=200, verbose_name='Название ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(help_text='Укажите автора рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(help_text='Укажите время готовки в минутах', verbose_name='Время готовки'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='Выберите изображение рецепта', upload_to='recipes/images', verbose_name='Изображение рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(help_text='Опишите способ приготовления', verbose_name='Способ приготовления'),
        ),
        migrations.AlterField(
            model_name='recipefav',
            name='recipe',
            field=models.ForeignKey(help_text='Укажите рецепт для добавление в избранное', on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipefav',
            name='user',
            field=models.ForeignKey(help_text='Укажите пользователя для избранного рецепта', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveIntegerField(help_text='Укажите количество ингредиента', verbose_name='Количество ингредиентов'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(help_text='Укажите ингредиент для рецепта', on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(help_text='Укажите рецепт для ингредиента', on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipetag',
            name='recipe',
            field=models.ForeignKey(help_text='Укажите рецепт для тега', on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='recipetag',
            name='tag',
            field=models.ForeignKey(help_text='Укажите тег для рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='recipes.tag', verbose_name='Тег'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(help_text='Введите цвет тега в HEX-кодировке', max_length=7, unique=True, verbose_name='Цвет тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='Введите название тега', max_length=200, unique=True, verbose_name='Название тега'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(help_text='Введите slug тега', max_length=200, unique=True, verbose_name='Slug тега'),
        ),
    ]
