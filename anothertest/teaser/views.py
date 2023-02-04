from django.http.response import HttpResponseRedirect
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Teaser
from .permissions import IsOwnerOrAdmin
from .serializers import (TeaserCreateSerializer, TeaserUpdateAdminSerializer,
                          TeaserUpdateSerializer, TeaserViewSerializer)


class TeaserViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Teaser.objects.all()

    def list(self, request, *args, **kwargs):
        """ Отдает список тизеров, в случае если пользователь
            не админ, перенаправляет на эндпоинт "/home" """

        if not self.request.user.is_staff:
            return HttpResponseRedirect("home")

        return super().list(request, *args, **kwargs)

    @action(detail=False)
    def home(self, request: Request):
        """ Отображает список тизеров пользователя """

        teasers = self.queryset.filter(author=request.user)

        if (page := self.paginate_queryset(teasers)) is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(teasers, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        """ Возвращает пользовательские сериализаторы
            на основе действий и ролей """
        if self.action == "create":
            return TeaserCreateSerializer

        if self.action in ("update", "partial_update"):
            return (
                TeaserUpdateAdminSerializer
                if self.request.user.is_staff
                else TeaserUpdateSerializer
            )

        return TeaserViewSerializer

    def perform_create(self, serializer):
        """ Автоматически присваивает авторство пользователю """
        serializer.save(author=self.request.user)
