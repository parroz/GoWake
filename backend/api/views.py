from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from .auxiliar_functions import get_leaderboards
from .models import Competition, Event, Official, Athlete, AthleteEvent, MatrixHeatSystem, LeaderBoard
from .pagination import CompetitionsAppPagination
from .serializers import CompetitionSerializer, EventSerializer, OfficialSerializer, AthleteSerializer, \
    AthleteEventSerializer, UploadFromXml, CompetitionAppSerializer, CompetitionsAppSerializer, \
    MatrixHeatSystemSerializer, GenerateHeatSystem, InsertAllSerializer, LeaderboardSerializer, LadderSystem
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


class LeaderBoardsAPIView(generics.ListAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = LeaderBoard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(competition=self.kwargs.get('competition_pk'))
        return self.queryset.all()


def score_qlf(data):
    data['Q_global_Intensity_score'] = round((data['Q_1st_judge_Intensity_score'] + data[
        'Q_2nd_judge_Intensity_score'] + data['Q_3rd_judge_Intensity_score']) / 3, 1)

    data['Q_global_execution_score'] = round((data['Q_1st_judge_Execution_score'] + data[
        'Q_2nd_judge_Execution_score'] + data['Q_3rd_judge_Execution_score']) / 3, 1)

    data['Q_global_composition_score'] = round((data['Q_1st_judge_Composition_score'] + data[
        'Q_2nd_judge_Composition_score'] + data['Q_3rd_judge_Composition_score']) / 3, 1)

    data['Q_1st_judge_global_score'] = round((data['Q_1st_judge_Intensity_score'] + data[
        'Q_1st_judge_Execution_score'] + data['Q_1st_judge_Composition_score']) / 3, 1)

    data['Q_2nd_judge_global_score'] = round((data['Q_2nd_judge_Intensity_score'] + data[
        'Q_2nd_judge_Execution_score'] + data['Q_2nd_judge_Composition_score']) / 3, 1)

    data['Q_3rd_judge_global_score'] = round((data['Q_3rd_judge_Intensity_score'] + data[
        'Q_3rd_judge_Execution_score'] + data['Q_3rd_judge_Composition_score']) / 3, 1)

    data['Q_global_score'] = round(
        (data['Q_1st_judge_global_score'] + data['Q_2nd_judge_global_score'] + data['Q_3rd_judge_global_score']) / 3, 1)
    data['Q_global_Intensity_pontuation'] = round(data['Q_global_Intensity_score'] * 3.34, 1)
    data['Q_global_execution_pontuation'] = round(data['Q_global_execution_score'] * 3.33, 1)
    data['Q_global_composition_pontuation'] = round(data['Q_global_composition_score'] * 3.33, 1)

    data['Q_global_pontuation'] = round(
        data['Q_global_Intensity_pontuation'] + data['Q_global_execution_pontuation'] + data[
            'Q_global_composition_pontuation'], 1)

    return data


def score_lcq(data):
    data['LCQ_global_Intensity_score'] = round((data['LCQ_1st_judge_Intensity_score'] + data[
        'LCQ_2nd_judge_Intensity_score'] + data['LCQ_3rd_judge_Intensity_score']) / 3, 1)
    data['LCQ_global_execution_score'] = round((data['LCQ_1st_judge_Execution_score'] + data[
        'LCQ_2nd_judge_Execution_score'] + data['LCQ_3rd_judge_Execution_score']) / 3, 1)
    data['LCQ_global_composition_score'] = round((data['LCQ_1st_judge_Composition_score'] + data[
        'LCQ_2nd_judge_Composition_score'] + data['LCQ_3rd_judge_Composition_score']) / 3, 1)
    data['LCQ_1st_judge_global_score'] = round((data['LCQ_1st_judge_Intensity_score'] + data[
        'LCQ_1st_judge_Execution_score'] + data['LCQ_1st_judge_Composition_score']) / 3, 1)
    data['LCQ_2nd_judge_global_score'] = round((data['LCQ_2nd_judge_Intensity_score'] + data[
        'LCQ_2nd_judge_Execution_score'] + data['LCQ_2nd_judge_Composition_score']) / 3, 1)
    data['LCQ_3rd_judge_global_score'] = round((data['LCQ_3rd_judge_Intensity_score'] + data[
        'LCQ_3rd_judge_Execution_score'] + data['LCQ_3rd_judge_Composition_score']) / 3, 1)
    data['LCQ_global_score'] = round((data['LCQ_1st_judge_global_score'] + data['LCQ_2nd_judge_global_score'] + data[
        'LCQ_3rd_judge_global_score']) / 3, 1)
    data['LCQ_global_Intensity_pontuation'] = round(data['LCQ_global_Intensity_score'] * 3.34, 1)
    data['LCQ_global_execution_pontuation'] = round(data['LCQ_global_execution_score'] * 3.33, 1)
    data['LCQ_global_composition_pontuation'] = round(data['LCQ_global_composition_score'] * 3.33, 1)
    data['LCQ_global_pontuation'] = round(
        data['LCQ_global_Intensity_pontuation'] + data['LCQ_global_execution_pontuation'] + data[
            'LCQ_global_composition_pontuation'], 1)

    return data


def score_qrt_final(data):
    data['QrtFinal_global_Intensity_score'] = round((data['QrtFinal_1st_judge_Intensity_score'] + data[
        'QrtFinal_2nd_judge_Intensity_score'] + data['QrtFinal_3rd_judge_Intensity_score']) / 3, 1)
    data['QrtFinal_global_execution_score'] = round((data['QrtFinal_1st_judge_Execution_score'] + data[
        'QrtFinal_2nd_judge_Execution_score'] + data['QrtFinal_3rd_judge_Execution_score']) / 3, 1)
    data['QrtFinal_global_composition_score'] = round((data['QrtFinal_1st_judge_Composition_score'] + data[
        'QrtFinal_2nd_judge_Composition_score'] + data['QrtFinal_3rd_judge_Composition_score']) / 3, 1)
    data['QrtFinal_1st_judge_global_score'] = round((data['QrtFinal_1st_judge_Intensity_score'] + data[
        'QrtFinal_1st_judge_Execution_score'] + data['QrtFinal_1st_judge_Composition_score']) / 3, 1)
    data['QrtFinal_2nd_judge_global_score'] = round((data['QrtFinal_2nd_judge_Intensity_score'] + data[
        'QrtFinal_2nd_judge_Execution_score'] + data['QrtFinal_2nd_judge_Composition_score']) / 3, 1)
    data['QrtFinal_3rd_judge_global_score'] = round((data['QrtFinal_3rd_judge_Intensity_score'] + data[
        'QrtFinal_3rd_judge_Execution_score'] + data['QrtFinal_3rd_judge_Composition_score']) / 3, 1)
    data['QrtFinal_global_score'] = round((data['QrtFinal_1st_judge_global_score'] + data[
        'QrtFinal_2nd_judge_global_score'] + data['QrtFinal_3rd_judge_global_score']) / 3, 1)
    data['QrtFinal_global_Intensity_pontuation'] = round(data['QrtFinal_global_Intensity_score'] * 3.34, 1)
    data['QrtFinal_global_execution_pontuation'] = round(data['QrtFinal_global_execution_score'] * 3.33, 1)
    data['QrtFinal_global_composition_pontuation'] = round(data['QrtFinal_global_composition_score'] * 3.33, 1)
    data['QrtFinal_global_pontuation'] = round(
        data['QrtFinal_global_Intensity_pontuation'] + data['QrtFinal_global_execution_pontuation'] + data[
            'QrtFinal_global_composition_pontuation'], 1)

    return data


def score_semi_final(data):
    data['SemiFinal_global_Intensity_score'] = round((data['SemiFinal_1st_judge_Intensity_score'] + data[
        'SemiFinal_2nd_judge_Intensity_score'] + data['SemiFinal_3rd_judge_Intensity_score']) / 3, 1)
    data['SemiFinal_global_execution_score'] = round((data['SemiFinal_1st_judge_Execution_score'] + data[
        'SemiFinal_2nd_judge_Execution_score'] + data['SemiFinal_3rd_judge_Execution_score']) / 3, 1)
    data['SemiFinal_global_composition_score'] = round((data['SemiFinal_1st_judge_Composition_score'] + data[
        'SemiFinal_2nd_judge_Composition_score'] + data['SemiFinal_3rd_judge_Composition_score']) / 3, 1)
    data['SemiFinal_1st_judge_global_score'] = round((data['SemiFinal_1st_judge_Intensity_score'] + data[
        'SemiFinal_1st_judge_Execution_score'] + data['SemiFinal_1st_judge_Composition_score']) / 3, 1)
    data['SemiFinal_2nd_judge_global_score'] = round((data['SemiFinal_2nd_judge_Intensity_score'] + data[
        'SemiFinal_2nd_judge_Execution_score'] + data['SemiFinal_2nd_judge_Composition_score']) / 3, 1)
    data['SemiFinal_3rd_judge_global_score'] = round((data['SemiFinal_3rd_judge_Intensity_score'] + data[
        'SemiFinal_3rd_judge_Execution_score'] + data['SemiFinal_3rd_judge_Composition_score']) / 3, 1)
    data['SemiFinal_global_score'] = round((data['SemiFinal_1st_judge_global_score'] + data[
        'SemiFinal_2nd_judge_global_score'] + data['SemiFinal_3rd_judge_global_score']) / 3, 1)
    data['SemiFinal_global_Intensity_pontuation'] = round(data['SemiFinal_global_Intensity_score'] * 3.34, 1)
    data['SemiFinal_global_execution_pontuation'] = round(data['SemiFinal_global_execution_score'] * 3.33, 1)
    data['SemiFinal_global_composition_pontuation'] = round(data['SemiFinal_global_composition_score'] * 3.33, 1)
    data['SemiFinal_global_pontuation'] = round(
        data['SemiFinal_global_Intensity_pontuation'] + data['SemiFinal_global_execution_pontuation'] + data[
            'SemiFinal_global_composition_pontuation'], 1)

    return data


def score_final(data):
    data['Final_global_Intensity_score'] = round((data['Final_1st_judge_Intensity_score'] + data[
        'Final_2nd_judge_Intensity_score'] + data['Final_3rd_judge_Intensity_score']) / 3, 1)
    data['Final_global_execution_score'] = round((data['Final_1st_judge_Execution_score'] + data[
        'Final_2nd_judge_Execution_score'] + data['Final_3rd_judge_Execution_score']) / 3, 1)
    data['Final_global_composition_score'] = round((data['Final_1st_judge_Composition_score'] + data[
        'Final_2nd_judge_Composition_score'] + data['Final_3rd_judge_Composition_score']) / 3, 1)
    data['Final_1st_judge_global_score'] = round((data['Final_1st_judge_Intensity_score'] + data[
        'Final_1st_judge_Execution_score'] + data['Final_1st_judge_Composition_score']) / 3, 1)
    data['Final_2nd_judge_global_score'] = round((data['Final_2nd_judge_Intensity_score'] + data[
        'Final_2nd_judge_Execution_score'] + data['Final_2nd_judge_Composition_score']) / 3, 1)
    data['Final_3rd_judge_global_score'] = round((data['Final_3rd_judge_Intensity_score'] + data[
        'Final_3rd_judge_Execution_score'] + data['Final_3rd_judge_Composition_score']) / 3, 1)
    data['Final_global_score'] = round((data['Final_1st_judge_global_score'] + data['Final_2nd_judge_global_score'] +
                                        data['Final_3rd_judge_global_score']) / 3, 1)
    data['Final_global_Intensity_pontuation'] = round(data['Final_global_Intensity_score'] * 3.34, 1)
    data['Final_global_execution_pontuation'] = round(data['Final_global_execution_score'] * 3.33, 1)
    data['Final_global_composition_pontuation'] = round(data['Final_global_composition_score'] * 3.33, 1)
    data['Final_global_pontuation'] = round(
        data['Final_global_Intensity_pontuation'] + data['Final_global_execution_pontuation'] + data[
            'Final_global_composition_pontuation'], 1)

    return data


def update_placement(competition, competition_round, category_in_competition, gender, id):
    global_pontuation = '-Q_global_pontuation'

    leaderboards = get_leaderboards(competition, category_in_competition, gender, global_pontuation, id,
                                    competition_round)

    for index, leaderboard in enumerate(leaderboards, start=1):
        leaderboard.Q_placement = index
        leaderboard.global_pontuation = leaderboard.Q_global_pontuation
        leaderboard.save()


class LeaderBoardAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = LeaderBoard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_object(self):
        if self.kwargs.get('competition_pk'):
            return get_object_or_404(self.get_queryset(),
                                     competition=self.kwargs.get('competition_pk'),
                                     pk=self.kwargs.get('leaderboard_pk'))
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get('leaderboard_pk'))

    def put(self, request, competition_pk, leaderboard_pk):
        print("update judgesheet")
        leaderboard = LeaderBoard.objects.get(pk=leaderboard_pk)
        username = self.request.user
        competition = Competition.objects.get(id=competition_pk)
        athlete = Athlete.objects.get(id=request.data.get('athlete_id'))
        competition_round = request.data.get('round')
        print("update leaderboard 1")
        score_qlf(request.data)
        print("update leaderboard 2")
        serializer = LeaderboardSerializer(leaderboard, data=request.data)
        print("update leaderboard 3")
        if serializer.is_valid():
            serializer.save(competition=competition, username=username, athlete=athlete)
            if competition_round:
                update_placement(competition, competition_round, request.data.get('athlete_category_in_competition'),
                                 request.data.get('athlete_gender'), request.data.get('id'))

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class CompetitionsAppAPIView(generics.ListAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Competition.objects.all()
    serializer_class = CompetitionsAppSerializer
    filter_backends = [DjangoFilterBackend]
    # pagination_class = CompetitionsAppPagination
    filterset_fields = ['code', 'organizing_country']

    def list(self, request, *args, **kwargs):
        competitions = self.get_queryset()  # Retrieve all competitions
        serializer = self.get_serializer(competitions, many=True)  # Serialize competitions
        list_competitions = []
        for competition in competitions:
            officials = Official.objects.filter(competition=competition.id)
            for official in officials:
                if official.iwwfid == self.kwargs.get('iwwf_id'):
                    list_competitions.append(competition)
                    break

        filtered_serializer = self.get_serializer(list_competitions, many=True)  # Serialize filtered competitions
        return Response({"results": filtered_serializer.data, "count": len(filtered_serializer.data)})

    def get_queryset(self):
        return Competition.objects.all()


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


class CompetitionDetailAppAPIView(generics.RetrieveAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = Competition.objects.all()
    serializer_class = CompetitionAppSerializer


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
def generate_heat_system(request):
    serializer = GenerateHeatSystem(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Heat system generated successfully."}, status=status.HTTP_201_CREATED)
    else:
        return Response({"ERROR": "Heat system was not generated."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def ladder_system(request):
    serializer = LadderSystem(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Ladder system generated successfully."}, status=status.HTTP_201_CREATED)
    else:
        return Response({"ERROR": "Ladder system was not generated."}, status=status.HTTP_400_BAD_REQUEST)


class LeaderBoardsCategoryAPIView(generics.ListAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = LeaderBoard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        if self.kwargs.get('competition_pk'):
            return self.queryset.filter(competition=self.kwargs.get('competition_pk'),
                                        athlete_category_in_competition=self.kwargs.get('category'),
                                        round=self.kwargs.get('round'),
                                        Q_Heat_number=self.kwargs.get('heat_number'),
                                        athlete_gender=self.kwargs.get('gender')).order_by('Q_Starting_list')
        return self.queryset.all()


# @api_view(['GET'])
# def get_leaderboards_by_category(request):
#     category = request.GET.get('category')
#     round = request.GET.get('round')
#     gender = request.GET.get('gender')
#     competition_id = request.GET.get('competition_pk')
#
#     leaderboards = LeaderBoard.objects.filter(
#         category=category,
#         round=round,
#         gender=gender,
#         competition_id=competition_id
#     )
#
#     serializer = LeaderboardSerializer(leaderboards, many=True)
#     return Response(serializer.data, status=200)


@api_view(['POST'])
def insert_all_view(request):
    serializer = InsertAllSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def create_competition_from_xml(request):
    serializer = UploadFromXml(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatrixHeatSystemAPIView(generics.ListCreateAPIView):
    permission_classes = (permissions.DjangoModelPermissions,)
    queryset = MatrixHeatSystem.objects.all()
    serializer_class = MatrixHeatSystemSerializer
