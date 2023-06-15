from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
  #  list_filter = ('name', 'measurement_unit')


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'author', 'text', 'cooking_time', 'image', 'date'
    )
    search_fields = ('name', 'author', 'text', 'cooking_time')
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favarite_count',)
    inlines = (RecipeIngredientsInLine,)

    def favarite_count(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngridientsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')
