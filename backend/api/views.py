from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from .models import Competition, Event, Official, Athlete, AthleteEvent
from .serializers import CompetitionSerializer, EventSerializer, OfficialSerializer, AthleteSerializer, \
    AthleteEventSerializer, UploadFromXml
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


# from roles.models import Official
# from roles.serializers import UserSerializer
class AthleteEventsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = AthleteEvent.objects.all()
    serializer_class = AthleteEventSerializer

    def get_queryset(self):
        if self.kwargs.get('event_pk'):
            return self.queryset.filter(event=self.kwargs.get('event_pk'))
        return self.queryset.all()

    def perform_create(self, serializer):
        username = self.request.user
        event = Event.objects.get(id=self.kwargs.get('event_pk'))
        competition = Competition.objects.get(id=self.kwargs.get('competition_pk'))
        serializer.save(competition=competition, event=event, username=username)


class AthleteEventAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = AthleteEvent.objects.all()
    serializer_class = AthleteEventSerializer

    def get_object(self):
        if self.kwargs.get('event_pk'):
            return get_object_or_404(self.get_queryset(),
                                     competition=self.kwargs.get('competition_pk'),
                                     event=self.kwargs.get('event_pk'),
                                     pk=self.kwargs.get('athlete_event_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('athlete_event_pk'))

    def put(self, request, competition_pk, event_pk, athlete_event_pk):
        event_athlete = AthleteEvent.objects.get(pk=athlete_event_pk)
        username = self.request.user
        event = Event.objects.get(id=event_pk)
        competition = Competition.objects.get(id=competition_pk)
        serializer = AthleteEventSerializer(event_athlete, data=request.data)
        if serializer.is_valid():
            serializer.save(competition=competition, event=event, username=username)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AthletesAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(competition=self.kwargs.get('competition_pk'))
        return self.queryset.all()

    def perform_create(self, serializer):
        username = self.request.user
        review_queryset = Athlete.objects.filter(
            Q(competition=self.kwargs.get('competition_pk')) & Q(fed_id=self.request.data['fed_id']))
        if review_queryset.exists():
            raise ValidationError("This fed id (" + self.request.data['fed_id'] + ") already exist!")

        event_ids = [event['id'] for event in self.request.data['events']]
        events = AthleteEvent.objects.filter(id__in=event_ids)
        # ids = self.request.data['events'].split(',')
        # events = AthleteEvent.objects.filter(pk__in=id_list)
        competition = Competition.objects.get(id=self.kwargs.get('competition_pk'))
        serializer.save(competition=competition, username=username, events=events)


class AthleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('athlete_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('athlete_pk'))

    def put(self, request, competition_pk, athlete_pk):
        athlete = Athlete.objects.get(pk=athlete_pk)
        username = self.request.user
        competition = Competition.objects.get(id=competition_pk)
        serializer = AthleteSerializer(athlete, data=request.data)
        review_queryset = Athlete.objects.filter(Q(fed_id=self.request.data['fed_id']) & ~Q(id=athlete_pk))
        if review_queryset.exists():
            raise ValidationError("This fed id (" + self.request.data['fed_id'] + ") already exist!")
        if serializer.is_valid():
            event_ids = [event['id'] for event in self.request.data['events']]
            events = AthleteEvent.objects.filter(id__in=event_ids)
            serializer.save(competition=competition, username=username, events=events)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficialAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('official_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('official_pk'))

    def put(self, request, competition_pk, official_pk):
        official = Official.objects.get(pk=official_pk)
        username = self.request.user
        competition = Competition.objects.get(id=competition_pk)
        serializer = OfficialSerializer(official, data=request.data)
        review_queryset = Official.objects.filter(Q(iwwfid=self.request.data['iwwfid']) & ~Q(id=official_pk))
        if review_queryset.exists():
            raise ValidationError("This iwwf id (" + self.request.data['iwwfid'] + ") already exist!")
        if serializer.is_valid():
            serializer.save(competition=competition, username=username)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfficialsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Official.objects.all()
    serializer_class = OfficialSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(competition=self.kwargs.get('competition_pk'))
        return self.queryset.all()

    def perform_create(self, serializer):
        username = self.request.user
        review_queryset = Official.objects.filter(
            Q(competition=self.kwargs.get('competition_pk')) & Q(iwwfid=self.request.data['iwwfid']))
        if review_queryset.exists():
            raise ValidationError("This iwwf id (" + self.request.data['iwwfid'] + ") already exist!")

        competition = Competition.objects.get(id=self.kwargs.get('competition_pk'))
        serializer.save(competition=competition, username=username)


class EventsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    serializer_class = EventSerializer

    def get_queryset(self):
        pk = self.kwargs['competition_pk']
        return Event.objects.filter(competition=pk)

    def perform_create(self, serializer):
        competition_pk = self.kwargs.get('competition_pk')
        username = self.request.user

        competition = Competition.objects.get(id=competition_pk)
        serializer.save(competition=competition, username=username)


class EventAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('event_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('event_pk'))

    def put(self, request, competition_pk, event_pk):
        event = Event.objects.get(pk=event_pk)
        username = self.request.user
        competition = Competition.objects.get(id=competition_pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save(competition=competition, username=username)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompetitionsAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code', 'organizing_country']

    def get_queryset(self):
        return Competition.objects.all()

    def perform_create(self, serializer):
        username = self.request.user
        review_queryset = Competition.objects.filter(code=self.kwargs.get('code'))
        if review_queryset.exists():
            raise ValidationError("This code already exist!")

        serializer.save(username=username)


class CompetitionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer

    def put(self, request, pk):
        competition = Competition.objects.get(pk=pk)
        serializer = CompetitionSerializer(competition, data=request.data)
        username = self.request.user
        review_queryset = Competition.objects.filter(Q(code=self.kwargs.get('code')) & ~Q(id=pk))
        if review_queryset.exists():
            raise ValidationError("This code already exist!")
        if serializer.is_valid():
            serializer.save(username=username)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_competition_from_xml(request):
    serializer = UploadFromXml(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)