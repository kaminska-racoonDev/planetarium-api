from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from .models import ShowTheme

from .serializers import ShowThemeSerializer


User = get_user_model()


class ShowThemeAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admintest@testemail.com",
            password="admintestpassword"
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_show_theme(self):
        payload = {"name": "Black Holes"}
        url = reverse("planetarium_app:showtheme-list")
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShowTheme.objects.count(), 1)

    def test_update_show_theme(self):
        theme = ShowTheme.objects.create(name="Black Holes")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": theme.pk}
        )
        response = self.client.put(url, {"name": "Large Black Hole"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_show_theme(self):
        theme = ShowTheme.objects.create(name="Test")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": theme.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_themes_list(self):
        url = reverse("planetarium_app:showtheme-list")
        res = self.client.get(url)

        items = ShowTheme.objects.all()
        serializer = ShowThemeSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_show_theme_retrieve(self) -> None:
        item = ShowTheme.objects.create(name="Test")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": item.pk}
        )
        res = self.client.get(url)

        serializer = ShowThemeSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)


class ShowThemeUnauthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_show_theme_create(self):
        payload = {"name": "Black Holes"}
        url = reverse("planetarium_app:showtheme-list")
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_theme_update(self):
        theme = ShowTheme.objects.create(name="Black Holes")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": theme.pk}
        )
        response = self.client.put(url, {"name": "Large Black Hole"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_theme_delete(self):
        theme = ShowTheme.objects.create(name="Test")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": theme.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_themes_list(self):
        url = reverse("planetarium_app:showtheme-list")
        res = self.client.get(url)

        items = ShowTheme.objects.all()
        serializer = ShowThemeSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_show_theme_retrieve(self) -> None:
        item = ShowTheme.objects.create(name="Test")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": item.pk}
        )
        res = self.client.get(url)

        serializer = ShowThemeSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)


class ShowThemeAuthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@test.com",
            password="passtest123"
        )
        self.client.force_authenticate(user=self.user)

    def test_show_theme_create(self):
        payload = {"name": "Black Holes"}
        url = reverse("planetarium_app:showtheme-list")
        response = self.client.post(url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_show_theme_update(self):
        theme = ShowTheme.objects.create(name="Black Holes")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": theme.pk}
        )
        response = self.client.put(url, {"name": "Large Black Hole"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_show_theme_delete(self):
        theme = ShowTheme.objects.create(name="Test")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": theme.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_show_themes_list(self):
        url = reverse("planetarium_app:showtheme-list")
        res = self.client.get(url)

        items = ShowTheme.objects.all()
        serializer = ShowThemeSerializer(items, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_show_theme_retrieve(self) -> None:
        item = ShowTheme.objects.create(name="Test")
        url = reverse(
            "planetarium_app:showtheme-detail",
            kwargs={"pk": item.pk}
        )
        res = self.client.get(url)

        serializer = ShowThemeSerializer(item)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)
