from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

# Create your models here.
User = get_user_model()


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    themes = models.ManyToManyField("ShowTheme", through="AstronomyShowTheme")


class ShowTheme(models.Model):
    name = models.CharField(max_length=255)


class AstronomyShowTheme(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    show_theme = models.ForeignKey(ShowTheme, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("astronomy_show", "show_theme")


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE)
    planetarium_dome = models.ForeignKey(
        PlanetariumDome, on_delete=models.CASCADE
    )
    show_time = models.DateTimeField()


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("show_session", "row", "seat")
