from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Competition, Official, Athlete, Event, AthleteEvent
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
