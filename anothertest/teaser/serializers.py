from rest_framework.serializers import ModelSerializer, ValidationError

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
        if self.instance.status != Teaser.Status.PENDING:
            raise ValidationError(
                f"Невозможно изменить статус с {self.instance.status}"
            )
        return value

    class Meta:
        model = Teaser
        fields = "__all__"
