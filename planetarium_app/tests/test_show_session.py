from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from planetarium_app.tests.helpers import (
    create_show_session,
    create_planetarium_dome,
    create_astronomy_show,
    create_show_theme,
)

User = get_user_model()


class ShowSessionAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admintest@testemail.com",
            password="admintestpassword"
        )
        self.client.force_authenticate(user=self.admin)

    def test_show_session_list(self):
        create_show_session()
        create_show_session()

        url = reverse("planetarium_app:showsession-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_show_session_create(self):
        dome = create_planetarium_dome()
        show = create_astronomy_show()

        url = reverse("planetarium_app:showsession-list")
        payload = {
            "astronomy_show": show.pk,
            "planetarium_dome": dome.pk,
            "show_time": "2025-08-01T10:00:00Z"
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_show_session_retrieve(self):
        session = create_show_session()
        url = reverse(
            "planetarium_app:showsession-detail",
            kwargs={"pk": session.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_session_update(self):
        session = create_show_session()
        dome = create_planetarium_dome(name="New Dome")
        show = create_astronomy_show(title="New Show")

        url = reverse(
            "planetarium_app:showsession-detail",
            kwargs={"pk": session.pk}
        )
        payload = {
            "astronomy_show": show.pk,
            "planetarium_dome": dome.pk,
            "show_time": "2025-09-01T10:00:00Z"
        }
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_session_delete(self):
        session = create_show_session()
        url = reverse(
            "planetarium_app:showsession-detail",
            kwargs={"pk": session.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_by_title(self):
        show1 = create_astronomy_show(title="Mars Journey")
        show2 = create_astronomy_show(title="Black Holes")
        create_show_session(astronomy_show=show1)
        create_show_session(astronomy_show=show2)

        url = reverse("planetarium_app:showsession-list") + "?title=mars"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_theme(self):
        theme_sci = create_show_theme(name="Science")
        theme_space = create_show_theme(name="Space")
        show1 = create_astronomy_show(title="Mars Journey", themes=[theme_sci])
        show2 = create_astronomy_show(
            title="Black Holes", themes=[theme_space])
        create_show_session(astronomy_show=show1)
        create_show_session(astronomy_show=show2)

        url = reverse("planetarium_app:showsession-list") + \
            f"?themes={theme_sci.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ShowSessionUnauthAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_show_session_list(self):
        url = reverse("planetarium_app:showsession-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_session_create(self):
        dome = create_planetarium_dome()
        show = create_astronomy_show()

        url = reverse("planetarium_app:showsession-list")
        payload = {
            "astronomy_show": show.pk,
            "planetarium_dome": dome.pk,
            "show_time": "2025-08-01T10:00:00Z"
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_show_session_delete(self):
        session = create_show_session()
        url = reverse(
            "planetarium_app:showsession-detail",
            kwargs={"pk": session.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ShowSessionAuthNotAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_show_session_list(self):
        url = reverse("planetarium_app:showsession-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_session_create_forbidden(self):
        dome = create_planetarium_dome()
        show = create_astronomy_show()

        url = reverse("planetarium_app:showsession-list")
        payload = {
            "astronomy_show": show.pk,
            "planetarium_dome": dome.pk,
            "show_time": "2025-08-01T10:00:00Z"
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_show_session_delete_forbidden(self):
        session = create_show_session()
        url = reverse(
            "planetarium_app:showsession-detail",
            kwargs={"pk": session.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
