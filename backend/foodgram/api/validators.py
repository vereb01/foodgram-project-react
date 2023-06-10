import datetime

from rest_framework.serializers import ValidationError


def validate_year(value):
    """Валидатор даты"""

    if value > datetime.datetime.now().year:
        raise ValidationError('Дата указана некорректно!')
    return value


def validate_ingredients(self, value):
    if not value:
        raise ValidationError('Нужно добавить ингридиент.')
    for amount in value:
        if amount['amount'] <= 0:
            raise ValidationError(
                'Колличество ингредиентов должно быть больше 0'
            )
    return value
