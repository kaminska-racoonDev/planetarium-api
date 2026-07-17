from django.urls import path, include
from rest_framework import routers

from planetarium_app.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    ReservationViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("themes", ShowThemeViewSet)
router.register("astronomy_show", AstronomyShowViewSet)
router.register("reservation", ReservationViewSet)
router.register("planetarium_dome", PlanetariumDomeViewSet)
router.register("show_session", ShowSessionViewSet)
router.register("ticket", TicketViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "planetarium_app"
