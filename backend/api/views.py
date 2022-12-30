from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from .models import Competition, Event, Official, Athlete, AthleteEvent
from .serializers import CompetitionSerializer, EventSerializer, OfficialSerializer, AthleteSerializer, \
    AthleteEventSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import get_object_or_404


# from roles.models import Official
# from roles.serializers import UserSerializer
class AthleteEventsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = AthleteEvent.objects.all()
    serializer_class = AthleteEventSerializer

    def get_queryset(self):
        if self.kwargs.get('athlete_pk'):
            return self.queryset.filter(id_athlete=self.kwargs.get('athlete_pk'))
        return self.queryset.all()


class AthleteEventAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = AthleteEvent.objects.all()
    serializer_class = AthleteEventSerializer

    def get_object(self):
        if self.kwargs.get('athlete_pk'):
            return get_object_or_404(self.get_queryset(),
                                     id_athlete=self.kwargs.get('athlete_pk'),
                                     pk=self.kwargs.get('athlete_event_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('athlete_event_pk'))


class AthletesAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(id_competition=self.kwargs.get('competition_pk'))
        return self.queryset.all()


class AthleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     id_competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('athlete_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('athlete_pk'))


class OfficialAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     id_competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('official_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('official_pk'))


class OfficialsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(id_competition=self.kwargs.get('competition_pk'))
        return self.queryset.all()


class OfficialAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     id_competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('official_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('official_pk'))


class EventsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(id_competition=self.kwargs.get('competition_pk'))
        return self.queryset.all()


class EventAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     id_competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('event_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('event_pk'))


class CompetitionsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class CompetitionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        competition = self.get_object()
        serializer = EventSerializer(competition.events.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def officials(self, request, pk=None):
        competition = self.get_object()
        serializer = OfficialSerializer(competition.officials.all(), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def athletes(self, request, pk=None):
        competition = self.get_object()
        serializer = AthleteSerializer(competition.athletes.all(), many=True)
        return Response(serializer.data)


@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    # serializer = UserSerializer(data=request.data)
    # if serializer.is_valid(raise_exception=True):
    #     # instance = serializer.save()
    #     # instance = form.save()
    #     print(serializer.data)
    #     return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400)
