from django.contrib import admin

# Register your models here.
from .models import (
    Reservation,
    PlanetariumDome,
    AstronomyShow,
    ShowTheme,
    AstronomyShowTheme,
    ShowSession,
    Ticket,
)

admin.site.register(Reservation)
admin.site.register(PlanetariumDome)
admin.site.register(AstronomyShow)
admin.site.register(ShowTheme)
admin.site.register(AstronomyShowTheme)
admin.site.register(ShowSession)
admin.site.register(Ticket)
