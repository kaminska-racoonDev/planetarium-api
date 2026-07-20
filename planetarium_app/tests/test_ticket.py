from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from tests.helpers import (
    create_ticket,
    create_show_session,
    create_reservation,
)

User = get_user_model()


class TicketAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admintest@testemail.com",
            password="admintestpassword"
        )
        self.client.force_authenticate(user=self.admin)
        self.reservation = create_reservation(user=self.admin)
        self.session = create_show_session()

    def test_ticket_list(self):
        create_ticket(reservation=self.reservation, show_session=self.session)
        create_ticket(reservation=self.reservation,
                      show_session=self.session, row=1, seat=2)

        url = reverse("planetarium_app:ticket-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ticket_create(self):
        url = reverse("planetarium_app:ticket-list")
        payload = {
            "row": 2,
            "seat": 3,
            "show_session": self.session.pk,
            "reservation": self.reservation.pk,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_retrieve(self):
        ticket = create_ticket(
            reservation=self.reservation,
            show_session=self.session
        )
        url = reverse(
            "planetarium_app:ticket-detail",
            kwargs={"pk": ticket.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TicketUnauthAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_ticket_list(self):
        url = reverse("planetarium_app:ticket-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ticket_create(self):
        url = reverse("planetarium_app:ticket-list")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TicketAuthNotAdminAccessTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="user@test.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        self.reservation = create_reservation(user=self.user)
        self.session = create_show_session()

    def test_ticket_list(self):
        url = reverse("planetarium_app:ticket-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ticket_create(self):
        url = reverse("planetarium_app:ticket-list")
        payload = {
            "row": 1,
            "seat": 1,
            "show_session": self.session.pk,
            "reservation": self.reservation.pk,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_ticket_double_booking(self):
        create_ticket(
            reservation=self.reservation,
            show_session=self.session,
            row=1,
            seat=1
        )
        url = reverse("planetarium_app:ticket-list")
        payload = {
            "row": 1,
            "seat": 1,
            "show_session": self.session.pk,
            "reservation": self.reservation.pk,
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
