from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class CategoryChoice(IntegerChoices):
    FIRST = 1, _("Первая категория")
    SECOND = 2, _("Вторая категория")
    THIRD = 3, _("Третья категория")


class StatusChoice(IntegerChoices):
    PENDING = 1, _("На рассмотрении")
    PAID = 2, _("Оплачен")
    REJECTED = 3, _("Отклонен")
