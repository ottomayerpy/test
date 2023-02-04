from anothertest.teaser.choices import StatusChoice
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Teaser, Person


class AccountTests(APITestCase):

    client: APIClient

    # Задаём настройки для админа и пользователя
    def setUp(self):

        self.admin = Person.objects.create(username="admin", is_staff=True)
        self.admin.set_password("admin_pass")
        self.admin.save()

        self.user = Person.objects.create(username="user", is_staff=False)
        self.user.set_password("user_pass")
        self.user.save()

    # Создание тизера
    def _create_teaser(self, user: Person, data: dict):
        self.client.force_authenticate(user=user)
        return self.client.post(reverse("teaser-list"), data=data)

    # Достаём список тизеров в зависимости от роли пользователя
    def _list_teasers(self, user: Person, home: bool = False):
        self.client.force_authenticate(user)
        return self.client.get(
            reverse("teaser-home" if home else "teaser-list")
        )

    # Тест создания тизера администратором
    def test_create_admin_teaser(self):
        data = {
            "title": "Admin Teaser",
            "description": "Admin description text",
        }

        response = self._create_teaser(self.admin, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertEqual(response.json()["description"], data["description"])

    # Тест создания тизера пользователем
    def test_create_user_teaser(self):
        data = {
            "title": "User Teaser",
            "description": "User description text",
        }

        response = self._create_teaser(self.user, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], data["title"])
        self.assertEqual(response.json()["description"], data["description"])

    # Тест получения списка тизеров админом(нет тизеров)
    def test_list_teasers_admin_no_teasers(self):
        response = self._list_teasers(self.admin)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    # Тест перенаправляющий пользователя на домашнюю страницу
    def test_list_teasers_user_redirect(self):
        response = self._list_teasers(self.user)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    # Тест получения списка тизеров пользователем
    # с домашней страницы (тизеров нет)
    def test_home_teasers_user_no_teasers(self):
        response = self._list_teasers(self.user, True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    # Тест получения списка тизеров админом
    # с домашней страницы (тизеров нет)
    def test_home_teasers_admin_no_teasers(self):
        response = self._list_teasers(self.admin, True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    # Тест получения списка тизеров админом (тизеры есть)
    def test_list_teasers_admin_has_teasers(self):
        self.test_create_admin_teaser()
        self.test_create_user_teaser()

        response = self._list_teasers(self.admin)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    # Тест получения списка тизеров админом
    # с домашней страницы (тизеры есть)
    def test_home_teasers_admin_has_teasers(self):
        self.test_create_admin_teaser()

        response = self._list_teasers(self.admin)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    # Тест получения списка тизеров (тизеры есть)
    def test_list_teasers_user_has_teasers(self):
        self.test_create_user_teaser()
        self.test_create_admin_teaser()

        response = self._list_teasers(self.user)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        response = self._list_teasers(self.user, True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    # Тест смены статуса тизера пользователем
    def test_user_change_teaser_status_unchanged(self):
        self.test_create_user_teaser()
        teaser = Teaser.objects.filter(author=self.user).first()

        url = "%s%s/" % (reverse("teaser-list"), str(teaser.id))
        data = {
            "title": "Status not changed",
            "status": StatusChoice.PAID,
        }

        self.client.force_authenticate(user=self.user)
        self.client.patch(url, data=data)

        teaser.refresh_from_db()

        self.assertEqual(teaser.title, data["title"])
        self.assertEqual(teaser.status, StatusChoice.PENDING)

    # Тест смены статуса тизера
    def test_admin_change_teaser_status_changed(self):
        self.test_create_user_teaser()
        teaser = Teaser.objects.filter(author=self.user).first()

        url = "%s%s/" % (reverse("teaser-list"), str(teaser.id))
        data = {
            "title": "Status will be changed",
            "status": StatusChoice.PAID,
        }

        self.client.force_authenticate(user=self.admin)
        self.client.patch(url, data=data)

        teaser.refresh_from_db()

        self.assertEqual(teaser.title, data["title"])
        self.assertEqual(teaser.status, StatusChoice.PAID)

    # Тест смены залоченого статуса
    def test_admin_change_teaser_status_changed_locked(self):
        self.test_create_user_teaser()
        teaser = Teaser.objects.filter(author=self.user).first()

        url = "%s%s/" % (reverse("teaser-list"), str(teaser.id))

        self.client.force_authenticate(user=self.admin)
        self.client.patch(url, data={"status": StatusChoice.PAID})

        teaser.refresh_from_db()
        self.assertEqual(teaser.status, StatusChoice.PAID)

        response = self.client.patch(
            url, data={"status": StatusChoice.PENDING})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        teaser.refresh_from_db()
        self.assertEqual(teaser.status, StatusChoice.PAID)
