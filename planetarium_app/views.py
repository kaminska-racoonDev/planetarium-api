from rest_framework import viewsets, mixins
from planetarium_app.permissions import (
    IsAdminOrReadOnly,
)
from rest_framework.permissions import IsAuthenticated
from planetarium_app.serializers import (
    ShowThemeSerializer,
    ShowSessionListSerializer,
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    ReservationSerializer,
    TicketSerializer,
    TicketListSerializer,
    ShowSessionSerializer,
    ShowSessionDetailSerializer,
    PlanetariumDomeSerializer,
)
from planetarium_app.models import (
    ShowTheme,
    AstronomyShow,
    Reservation,
    PlanetariumDome,
    ShowSession,
    Ticket,
)
from planetarium_app.utils import params_to_ints


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Retrieve the astronomy show with filters by title and themes"""
        title = self.request.query_params.get("title")
        themes = self.request.query_params.get("themes")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if themes:
            themes_ids = params_to_ints(themes)
            queryset = queryset.filter(themes__id__in=themes_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AstronomyShowListSerializer
        return AstronomyShowSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Retrieve the planetarium dome with filter by name"""
        name = self.request.query_params.get("name")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.distinct()


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """Retrieve the show session with filters by title, theme, show_time"""
        title = self.request.query_params.get("title")
        themes = self.request.query_params.get("themes")
        show_time = self.request.query_params.get("show_time")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(astronomy_show__title__icontains=title)

        if themes:
            themes_ids = params_to_ints(themes)
            queryset = queryset.filter(
                astronomy_show__themes__id__in=themes_ids)

        if show_time:
            queryset = queryset.filter(show_time__date=show_time)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        elif self.action == "retrieve":
            return ShowSessionDetailSerializer
        return ShowSessionSerializer


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TicketListSerializer
        return TicketSerializer
