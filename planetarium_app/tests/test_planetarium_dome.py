from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from .helpers import (
    create_planetarium_dome
)


User = get_user_model()


class PlanetetariumDomeAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admintest@testemail.com",
            password="admintestpassword"
        )
        self.client.force_authenticate(user=self.admin)

    def test_planeterium_dome_create(self):
        url = reverse("planetarium_app:planetariumdome-list")
        payload = {
            "name": "Main Dome",
            "rows": 10,
            "seats_in_row": 15
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_planetarium_dome_update(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        payload = {
            "name": "IMAX Dome",
            "rows": 16,
            "seats_in_row": 12
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planetarium_dome_patch(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        payload = {
            "name": "IMAX Dome"
        }
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planetarium_dome_delete(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_planetarium_dome_retrieve(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planetarium_dome_list(self):
        url = reverse("planetarium_app:planetariumdome-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlanetetariumDomeUnauthorizedAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_planeterium_dome_create(self):
        url = reverse("planetarium_app:planetariumdome-list")
        payload = {
            "name": "Main Dome",
            "rows": 10,
            "seats_in_row": 15
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planetarium_dome_update(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        payload = {
            "name": "IMAX Dome",
            "rows": 16,
            "seats_in_row": 12
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planetarium_dome_patch(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        payload = {
            "name": "IMAX Dome"
        }
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planetarium_dome_delete(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_planetarium_dome_retrieve(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planetarium_dome_list(self):
        url = reverse("planetarium_app:planetariumdome-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlanetetariumDomeAuthorizedhAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="usertest@testemail.com",
            password="usertestpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_planeterium_dome_create(self):
        url = reverse("planetarium_app:planetariumdome-list")
        payload = {
            "name": "Main Dome",
            "rows": 10,
            "seats_in_row": 15
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_planetarium_dome_update(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        payload = {
            "name": "IMAX Dome",
            "rows": 16,
            "seats_in_row": 12
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_planetarium_dome_patch(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        payload = {
            "name": "IMAX Dome"
        }
        response = self.client.patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_planetarium_dome_delete(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_planetarium_dome_retrieve(self):
        dome = create_planetarium_dome()
        url = reverse(
            "planetarium_app:planetariumdome-detail",
            kwargs={"pk": dome.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_planetarium_dome_list(self):
        url = reverse("planetarium_app:planetariumdome-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
