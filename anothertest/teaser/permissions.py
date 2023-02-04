from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import Teaser


class IsOwnerOrAdmin(BasePermission):
    """ Проверка на доступ к объекту - Создатель или Админ """

    def has_object_permission(self, request: Request, view, teaser: Teaser) -> bool:
        """ Проверка доступа к объекту

        Args:
            request (Request): Запрос
            view (TeaserViewSet): Не используется
            teaser (Teaser): Тизер

        Returns:
            bool: Доступ будет разрешенным если пользователь
                  является администратом, или автором тизера
        """
        return request.user.is_staff or teaser.author == request.user
