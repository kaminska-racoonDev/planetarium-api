from planetarium_app.models import (
    ShowTheme,
    AstronomyShow,
    AstronomyShowTheme,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket,
)
from django.utils import timezone


def create_show_theme(name="Test Theme"):
    return ShowTheme.objects.create(name=name)


def create_astronomy_show(title="Test Show", description="Test description", themes=None):
    show = AstronomyShow.objects.create(title=title, description=description)
    if themes:
        for theme in themes:
            AstronomyShowTheme.objects.create(
                astronomy_show=show, show_theme=theme)
    return show


def create_planetarium_dome(name="Test Dome", rows=10, seats_in_row=15):
    return PlanetariumDome.objects.create(
        name=name,
        rows=rows,
        seats_in_row=seats_in_row
    )


def create_show_session(astronomy_show=None, planetarium_dome=None, show_time=None):
    if astronomy_show is None:
        astronomy_show = create_astronomy_show()
    if planetarium_dome is None:
        planetarium_dome = create_planetarium_dome()
    if show_time is None:
        show_time = timezone.now()
    return ShowSession.objects.create(
        astronomy_show=astronomy_show,
        planetarium_dome=planetarium_dome,
        show_time=show_time
    )


def create_reservation(user):
    return Reservation.objects.create(user=user)


def create_ticket(reservation=None, show_session=None, row=1, seat=1):
    if show_session is None:
        show_session = create_show_session()
    return Ticket.objects.create(
        reservation=reservation,
        show_session=show_session,
        row=row,
        seat=seat
    )
