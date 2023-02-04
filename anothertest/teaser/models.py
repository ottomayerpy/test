from baseapp.models import AnotherBaseModel, TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import CategoryChoice, StatusChoice

User = get_user_model()


class Teaser(AnotherBaseModel, TimeStampedModel):
    title = models.CharField(verbose_name=_("Заголовок"), max_length=64)
    description = models.TextField(verbose_name=_("Описание"), max_length=256)
    author = models.ForeignKey(
        User, verbose_name=_("Автор"), on_delete=models.CASCADE)
    category = models.IntegerField(
        verbose_name=_("Категория"),
        choices=CategoryChoice.choices,
        default=CategoryChoice.FIRST,
    )
    status = models.IntegerField(
        verbose_name=_("Статус"),
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING,
    )

    class Meta:
        verbose_name = "Тизер"
        verbose_name_plural = "Тизеры"
