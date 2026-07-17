from rest_framework import serializers
from planetarium_app.models import (
    ShowTheme,
    AstronomyShow,
    Reservation,
    PlanetariumDome,
    ShowSession,
    Ticket,
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ["id", "name"]


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = AstronomyShow
        fields = [
            "id",
            "title",
            "description",
            "themes",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "created_at",
        ]


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = [
            "id",
            "name",
            "rows",
            "seats_in_row",
        ]


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show = AstronomyShowSerializer(read_only=False)
    planetarium_dome = PlanetariumDomeSerializer(read_only=False)

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time"
        ]


class TicketSerializer(serializers.ModelSerializer):
    show_session = AstronomyShowSerializer(
        many=True,
        read_only=False
    )
    reservation = ReservationSerializer(
        many=True,
        read_only=False
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "show_session",
            "reservation",
            "row",
            "seat",
        ]
