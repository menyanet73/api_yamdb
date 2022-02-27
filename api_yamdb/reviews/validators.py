from django.core.exceptions import ValidationError
from django.utils import timezone


def less_then_now_year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Нельзя добавить не вышедшее произведение!',
            params={'value': value}
        )
