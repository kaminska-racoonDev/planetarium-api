from planetarium_app.serializers import AstronomyShowListSerializer
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from planetarium_app.models import (
    AstronomyShow
)
from planetarium_app.tests.helpers import (
    create_show_theme,
    create_astronomy_show,
)


User = get_user_model()


class AstronomyShowAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admintest@testemail.com",
            password="admintestpassword"
        )
        self.client.force_authenticate(user=self.admin)

    def test_astronomy_show_create(self):
        theme = create_show_theme(name="Science")
        url = reverse("planetarium_app:astronomyshow-list")
        payload = {
            "title": "Mars Journey",
            "description": "...",
            "themes": [theme.id]
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_astronomy_show_list(self):
        create_astronomy_show(title="Mars Journey")
        create_astronomy_show(title="Black Holes")

        url = reverse("planetarium_app:astronomyshow-list")
        response = self.client.get(url)

        shows = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(shows, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_astronomy_show_retrieve(self):
        show = create_astronomy_show(title="Mars Journey")
        url = reverse(
            "planetarium_app:astronomyshow-detail",
            kwargs={"pk": show.pk}
        )
        response = self.client.get(url)
        serializer = AstronomyShowListSerializer(show)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_by_title(self):
        create_astronomy_show(title="Mars Journey")
        create_astronomy_show(title="Black Holes")

        url = reverse("planetarium_app:astronomyshow-list") + "?title=mars"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Mars Journey")

    def test_filter_by_theme(self):
        theme_sci = create_show_theme(name="Science")
        theme_space = create_show_theme(name="Space")

        create_astronomy_show(title="Mars Journey", themes=[theme_sci])
        create_astronomy_show(title="Black Holes", themes=[theme_space])

        url = reverse("planetarium_app:astronomyshow-list") + \
            f"?themes={theme_sci.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Mars Journey")

    def test_astronomy_show_update(self):
        show = create_astronomy_show(title="Mars Journey")
        theme = create_show_theme(name="Science")
        url = reverse(
            "planetarium_app:astronomyshow-detail",
            kwargs={"pk": show.pk}
        )
        payload = {
            "title": "Mars Journey Updated",
            "description": "...",
            "themes": [theme.id]
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_astronomy_show_delete(self):
        show = create_astronomy_show(title="Mars Journey")
        url = reverse(
            "planetarium_app:astronomyshow-detail",
            kwargs={"pk": show.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AstronomyShowUnauthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_astronomy_show_create(self):
        theme = create_show_theme()
        url = reverse("planetarium_app:astronomyshow-list")
        payload = {
            "title": "Mars Journey",
            "description": "...",
            "themes": [theme.id]
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_astronomy_show_list(self):
        url = reverse("planetarium_app:astronomyshow-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AstronomyShowAuthorizedTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_astronomy_show_create_forbidden(self):
        theme = create_show_theme()
        url = reverse("planetarium_app:astronomyshow-list")
        payload = {
            "title": "Mars Journey",
            "description": "...",
            "themes": [theme.id]
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_astronomy_show_list_allowed(self):
        url = reverse("planetarium_app:astronomyshow-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
