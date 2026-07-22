from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from tests.helpers import create_reservation

User = get_user_model()


class ReservationAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admintest@testemail.com",
            password="admintestpassword"
        )
        self.client.force_authenticate(user=self.admin)

    def test_reservation_list(self):
        create_reservation(user=self.admin)
        create_reservation(user=self.admin)

        url = reverse("planetarium_app:reservation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_reservation_create(self):
        url = reverse("planetarium_app:reservation-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reservation_delete(self):
        reservation = create_reservation(user=self.admin)
        url = reverse(
            "planetarium_app:reservation-detail",
            kwargs={"pk": reservation.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reservation_retrieve(self):
        reservation = create_reservation(user=self.admin)
        url = reverse(
            "planetarium_app:reservation-detail",
            kwargs={"pk": reservation.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReservationUnauthAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_reservation_list(self):
        url = reverse("planetarium_app:reservation-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reservation_create(self):
        url = reverse("planetarium_app:reservation-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReservationAuthAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="usertest@testemail.com",
            password="usertestpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_reservation_list_only_own(self):
        other_user = User.objects.create_user(
            email="other@test.com", password="pass"
        )
        create_reservation(user=self.user)
        create_reservation(user=self.user)
        create_reservation(user=other_user)

        url = reverse("planetarium_app:reservation-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_reservation_create(self):
        url = reverse("planetarium_app:reservation-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reservation_other_user_not_visible(self):
        other_user = User.objects.create_user(
            email="other@test.com", password="pass"
        )
        reservation = create_reservation(user=other_user)
        url = reverse(
            "planetarium_app:reservation-detail",
            kwargs={"pk": reservation.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
