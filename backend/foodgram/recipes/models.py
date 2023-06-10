from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from api.validators import validate_year

User = get_user_model()


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        verbose_name='Имя тега',
        max_length=150,
        unique=True
    )

    color = models.CharField(
        verbose_name='Цвет',
        help_text=('Введите код цвета в формате HEX (#ABCDEF)'),
        max_length=7,
        validators=(
            RegexValidator(
                regex=r'^#[A-Fa-f0-9]{3,6}$',
                code='wrong_hex_code',
                message='Цвет не в формате HEX'),
        )
    )
    slug = models.SlugField(
        'Slug',
        help_text='Введите заголовок тега',
        unique=True
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингридиенты"""

    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('pk',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/'
    )
    text = models.TextField(verbose_name='Текст')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(
            1, message='Минимальное время приготовления - 1!'
        )]
    )
    date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        validators=(validate_year,)
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date',)

    def __str__(self):
        return str(self.name)


class RecipeIngredient(models.Model):
    """Модель ингредиентов для рецепта"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(MinValueValidator(1),)
    )

    class Meta:
        verbose_name = 'Ингредиент для приготовления'
        verbose_name_plural = 'Ингредиенты для приготовления'
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'ingredient'), name='recipeingredient'),
        )

    def __str__(self):
        return f'{str(self.ingredient)} in {str(self.recipe)}-{self.amount}'


class Favourite(models.Model):
    """Модель Избранное"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourite'
            ),
        )

    def __str__(self):
        return f'{self.recipe} добавлен в избранное '


class ShoppingCart(models.Model):
    """Модель списка покупок"""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping'
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Список Покупок'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'Добавил в корзину {self.recipe}'
