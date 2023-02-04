from anothertest.settings import PAYOUT_AMOUNT
from rest_framework.serializers import ModelSerializer, ValidationError

from .choices import StatusChoice
from .models import Teaser


class TeaserCreateSerializer(ModelSerializer):
    """ Запрещает обычным пользователям менять поля
        "Статус" и "Автор" при создании тизера """

    class Meta:
        model = Teaser
        exclude = ["status", "author"]


class TeaserUpdateSerializer(ModelSerializer):
    """ Запрещает обычным пользователям менять поля
        "Статус" и "Автор" при обновлении тизера """

    # Вынесено в отдельный класс для последующего расширения
    class Meta:
        model = Teaser
        exclude = ["status", "author"]


class TeaserViewSerializer(ModelSerializer):
    """ Сериализует все поля модели """

    class Meta:
        model = Teaser
        fields = "__all__"


class TeaserUpdateAdminSerializer(ModelSerializer):
    """ Позволяет изменить все поля за исключением "Статус"
        при смене с "На рассмотрении" """

    def validate_status(self, value: str):
        if value != self.instance.status and self.instance.status != StatusChoice.PENDING:
            raise ValidationError(
                f"Невозможно изменить статус с {self.instance.get_status_display()}"
            )
        if value == StatusChoice.PAID and self.instance.status != StatusChoice.PAID:
            self.instance.author.wallet += PAYOUT_AMOUNT
            self.instance.author.save()
        return value

    class Meta:
        model = Teaser
        fields = "__all__"
