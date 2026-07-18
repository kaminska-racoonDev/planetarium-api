from rest_framework import serializers
from django.db import transaction
from planetarium_app.models import (
    ShowTheme,
    AstronomyShow,
    AstronomyShowTheme,
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
    themes = serializers.PrimaryKeyRelatedField(
        many=True,
        allow_empty=False,
        queryset=ShowTheme.objects.all()
    )

    class Meta:
        model = AstronomyShow
        fields = [
            "id",
            "title",
            "description",
            "themes",
        ]

    def create(self, validated_data):
        with transaction.atomic():
            themes_data = validated_data.pop("themes")
            astronomy_show = AstronomyShow.objects.create(**validated_data)
            for theme_data in themes_data:
                AstronomyShowTheme.objects.create(
                    astronomy_show=astronomy_show,
                    show_theme=theme_data)
            return astronomy_show


class AstronomyShowListSerializer(serializers.ModelSerializer):
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
    astronomy_show = serializers.PrimaryKeyRelatedField(
        queryset=AstronomyShow.objects.all()
    )
    planetarium_dome = serializers.PrimaryKeyRelatedField(
        queryset=PlanetariumDome.objects.all()
    )
    available_seats = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
            "available_seats",
        ]


class ShowSessionListSerializer(serializers.ModelSerializer):
    astronomy_show = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title",
    )
    planetarium_dome = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
        ]


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowListSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
            "available_seats",
        ]


class TicketSerializer(serializers.ModelSerializer):
    show_session = ShowSessionSerializer(
        read_only=True
    )
    reservation = ReservationSerializer(
        read_only=True
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


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer()
    reservation = ReservationSerializer()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "show_session",
            "row",
            "seat",
            "reservation"
        ]
