import random

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Competition, Official, Athlete, Event, AthleteEvent, MatrixHeatSystem, LeaderBoard
from rest_framework.serializers import Serializer, FileField
from rest_framework.fields import CurrentUserDefault

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        exclude = ['competition']


class OfficialSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)

    def validate_iwwf_id(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("iwwf id is a required field!")
        else:
            return value

    class Meta:
        model = Official
        exclude = ['competition']


class AthleteEventSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField(read_only=True)
    username = serializers.StringRelatedField(read_only=True)

    def validate_fed_id(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("fed_id is a required field!")
        else:
            return value

    class Meta:
        model = AthleteEvent
        exclude = ['competition']


class AthleteXmlSerializer(serializers.ModelSerializer):
    events = AthleteEventSerializer(many=True)
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Athlete
        exclude = ['competition']


class AthleteSerializer(serializers.ModelSerializer):
    events = AthleteEventSerializer(many=True, read_only=True)
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Athlete
        exclude = ['competition']


class CompetitionsAppSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Competition
        exclude = ['createAt', 'updateAt']


class CompetitionHeatSystemSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Competition
        exclude = ['createAt', 'updateAt', 'events', 'officials', 'athletes']


class CompetitionAppSerializer(serializers.ModelSerializer):
    athlete_events = AthleteEventSerializer(many=True, read_only=True)
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Competition
        exclude = ['createAt', 'updateAt']


class CompetitionSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    officials = OfficialSerializer(many=True, read_only=True)
    athletes = AthleteSerializer(many=True, read_only=True)
    username = serializers.StringRelatedField(read_only=True)

    def validate_code(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Code is a required field!")
        else:
            return value

    class Meta:
        model = Competition
        fields = '__all__'


def get_ranking(athletes):
    rankings = list(range(1, 9999 + 1))
    random.shuffle(rankings)
    for i, athlete in enumerate(athletes):
        athlete.ranking = rankings[i]
        athlete.save()

    return athletes.order_by('ranking')


class GenerateHeatSystem(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)
    athlete = AthleteSerializer(many=True, read_only=True)
    competition = CompetitionSerializer(many=True, read_only=True)
    events = AthleteEventSerializer(many=True, read_only=True)

    class Meta:
        model = LeaderBoard
        exclude = ['id']

    def create(self, validated_data):
        competition_id = self.context['request'].data.get('competition_id')
        try:
            competition = Competition.objects.get(id=competition_id)

        except Competition.DoesNotExist:
            raise serializers.ValidationError("Competition with id={} does not exist".format(competition_id))

        athlete_events = AthleteEvent.objects.filter(competition=competition)
        for athlete_event in athlete_events:
            print(athlete_event)
            athletesF = Athlete.objects.filter(events=athlete_event, gender='F')
            for athlete in athletesF:
                print(athlete)
        # athletes = Athlete.objects.filter(competition=competition)
        # athletes = get_ranking(athletes)
        # for athlete in athletes:
        # print(athlete)

        # leaderboard = LeaderBoard.objects.create(competition=competition, **validated_data)
        return


class UploadFromXml(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    officials = OfficialSerializer(many=True)
    athletes = AthleteXmlSerializer(many=True)
    username = serializers.StringRelatedField(read_only=True)
    athlete_events = AthleteEventSerializer(many=True)

    def validate_code(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Code is a required field!")
        else:
            return value

    class Meta:
        model = Competition
        fields = '__all__'

    def create(self, validated_data):
        officials_data = validated_data.pop('officials')
        events_data = validated_data.pop('events')
        athletes_data = validated_data.pop('athletes')
        athlete_events_data = validated_data.pop('athlete_events')
        user = self.context.get("request").user
        competition = Competition.objects.create(username=user, **validated_data)

        for official_data in officials_data:
            Official.objects.create(competition=competition, **official_data, username=user)

        for event_data in events_data:
            event = Event.objects.create(competition=competition, **event_data, username=user)
            for athlete_event in athlete_events_data:
                if athlete_event["code"] == event_data["code"]:
                    AthleteEvent.objects.create(competition=competition, event=event, **athlete_event, username=user)

        for athlete in athletes_data:
            ev = athlete.pop('events')
            codes = [event['code'] for event in ev]
            events = AthleteEvent.objects.filter(code__in=codes)
            athlete_obj = Athlete.objects.create(competition=competition, **athlete, username=user)
            athlete_obj.events.set(events)

        return competition


class InsertAllSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    officials = OfficialSerializer(many=True)
    athletes = AthleteXmlSerializer(many=True)
    username = serializers.StringRelatedField(read_only=True)

    def validate_code(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("Code is a required field!")
        else:
            return value

    class Meta:
        model = Competition
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get("request").user
        # Create Competition instance
        competition_data = validated_data.copy()
        events_data = competition_data.pop('events')
        jury_data = competition_data.pop('officials')
        athletes_data = competition_data.pop('athletes')
        competition = Competition.objects.create(**competition_data, username=user)

        # Create Event instances
        for event_data in events_data:
            Event.objects.create(competition=competition, **event_data, username=user)

        # Create Official instances
        for official_data in jury_data:
            Official.objects.create(competition=competition, **official_data, username=user)

        # Create Athlete instances
        for athlete_data in athletes_data:
            athlete_events_data = athlete_data.pop('events')
            athlete = Athlete.objects.create(competition=competition, **athlete_data, username=user)
            for athlete_event_data in athlete_events_data:
                event = Event.objects.get(code=athlete_event_data['code'])
                athlete_events = AthleteEvent.objects.filter(
                    competition=competition,
                    event=event,
                    real_category=athlete_event_data['real_category'],
                    category_in_competition=athlete_event_data['category_in_competition']
                )
                if not athlete_events.exists():
                    athlete.events.create(competition=competition, event=event, **athlete_event_data,
                                          username=user)

        return competition


class MatrixHeatSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixHeatSystem
        fields = '__all__'
