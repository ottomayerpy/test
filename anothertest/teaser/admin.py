from django.contrib import admin

from .choices import StatusChoice
from .models import Teaser


@admin.register(Teaser)
class TeaserAdmin(admin.ModelAdmin):

    # Поля отображающиеся в админке
    list_display = (
        "id",
        "title",
        "author",
        "description",
        "status",
        "created_time",
        "modified_time",
    )

    # Поля предполагающие филтрацию
    list_filter = (
        "status",
    )

    # Не изменяемые поля, только для чтения
    readonly_fields = [
        "id",
        "created_time",
        "modified_time",
    ]

    # Поля по которым происходит поиск
    search_fields = (
        "id",
        "title",
        "author__username",
        "description",
    )

    # Отображение тизеров на странице
    list_per_page = 20

    # Разделяет окно Создания и Редактирования на два сета:
    # Основная информация и Время
    fieldsets = (
        (
            "Main info",
            {
                "fields": ("id", ("title", "author"), "status", "description"),
                "description": "Все поля в этом блоке обязательны для заполнения",
            },
        ),
        (
            "Timestamps",
            {
                "fields": (
                    "created_time",
                    "modified_time",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, teaser: Teaser = None) -> list:
        """ Установка поля "Статус" только для чтения, после
            изменения статуса с "На рассмотрении" на другой

        Args:
            request (Request): Не используется
            teaser (Teaser, optional): Тизер. По умолчанию None.

        Returns:
            list: Модифицированный (или нет) список полей только для чтения
        """
        if not teaser or (teaser and teaser.status != StatusChoice.PENDING):
            return self.readonly_fields + ["status"]

        return self.readonly_fields
