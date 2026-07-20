from rest_framework import viewsets, mixins
from .permissions import (
    IsAdminOrIfAuthenticatedReadOnly,
    IsAdminOrReadOnly,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import (
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
from .models import (
    ShowTheme,
    AstronomyShow,
    Reservation,
    PlanetariumDome,
    ShowSession,
    Ticket,
)


class ShowThemeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AstronomyShowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the astronomy show with filters by title and themes"""
        title = self.request.query_params.get("title")
        themes = self.request.query_params.get("themes")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if themes:
            themes_ids = self._params_to_ints(themes)
            queryset = queryset.filter(themes__id__in=themes_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return AstronomyShowListSerializer
        return AstronomyShowSerializer


class PlanetariumDomeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the planetarium dome with filter by name"""
        name = self.request.query_params.get("name")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.distinct()


class ShowSessionViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the show session with filters by title, theme, show_time"""
        title = self.request.query_params.get("title")
        themes = self.request.query_params.get("themes")
        show_time = self.request.query_params.get("show_time")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(astronomy_show__title__icontains=title)

        if themes:
            themes_ids = self._params_to_ints(themes)
            queryset = queryset.filter(
                astronomy_show__themes__id__in=themes_ids)

        if show_time:
            queryset = queryset.filter(show_time__icontains=show_time)

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
