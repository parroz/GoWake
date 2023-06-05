import random

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Competition, Official, Athlete, Event, AthleteEvent, MatrixHeatSystem, LeaderBoard, Categorie
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


class LeaderboardSerializer(serializers.ModelSerializer):
    competition_leaderboard = CompetitionSerializer(many=False, read_only=True)
    athlete = AthleteSerializer(many=False, read_only=True)
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LeaderBoard
        fields = '__all__'


def get_ranking(athletes):
    rankings = list(range(1, 999 + 1))
    random.shuffle(rankings)
    for i, athlete in enumerate(athletes):
        athlete.ranking = rankings[i]
        real_category = Categorie.objects.filter(description=athlete.real_category).first()
        category_in_competition = Categorie.objects.filter(description=athlete.category_in_competition).first()
        print("athlete real_category " + str(athlete.real_category))
        print("athlete category_in_competition " + str(athlete.category_in_competition))
        print("real_category" + str(real_category))
        print("category_in_competition" + str(category_in_competition))
        if real_category.code < category_in_competition.code:
            print("athlete.ranking" + str(athlete.ranking))
            athlete.ranking = athlete.ranking * 0.75
            print("athlete.ranking * 75% " + str(athlete.ranking))
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
        user = self.context.get("request").user
        competition_id = self.context['request'].data.get('competition_id')
        try:
            competition = Competition.objects.get(id=competition_id)
            leader_board_delete = LeaderBoard.objects.filter(competition=competition)
            if leader_board_delete:
                leader_board_delete.delete()
        except Competition.DoesNotExist:
            raise serializers.ValidationError("Competition with id={} does not exist".format(competition_id))

        athlete_events = AthleteEvent.objects.filter(competition=competition)
        for athlete_event in athlete_events:
            print(athlete_event)
            athletes_female = Athlete.objects.filter(category_in_competition=athlete_event.category_in_competition,
                                                     gender='F')
            athletes_female = get_ranking(athletes_female)
            print('Female qtd ' + str(len(athletes_female)))

            print("Generate Female")
            start_position = 0
            heat_count = 0

            if len(athletes_female) > 0:
                heat_system_female = MatrixHeatSystem.objects.get(Riders=len(athletes_female))
                print(heat_system_female)
                riders_q_heat_list = [True, True,
                                      True, True, True
                    , True]
                heat = heat_system_female.Q_Heats
                if int(heat_system_female.Q_Heats) > 1:
                    heat_count = heat_system_female.Riders_Q_Heat1
                    heat = 1
                for athlete in athletes_female:
                    start_position += 1
                    leader_board = LeaderBoard()
                    leader_board.athlete = athlete
                    leader_board.username = user
                    leader_board.competition = competition
                    leader_board.ranking = athlete.ranking
                    leader_board.athlete_gender = athlete.gender
                    leader_board.athlete_category_in_competition = athlete.category_in_competition
                    leader_board.Q_Heat_number = heat_system_female.Q_Heats
                    leader_board.Q_Starting_list = start_position
                    leader_board.save()
                    if int(heat_system_female.Q_Heats) > 1 and riders_q_heat_list[0] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_female.Riders_Q_Heat2
                        riders_q_heat_list[0] = False
                        print("Riders_Q_Heat1")
                    if int(heat_system_female.Q_Heats) > 1 and riders_q_heat_list[1] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_female.Riders_Q_Heat3
                        riders_q_heat_list[1] = False
                        print("Riders_Q_Heat2")
                    if int(heat_system_female.Q_Heats) > 1 and riders_q_heat_list[2] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_female.Riders_Q_Heat4
                        riders_q_heat_list[2] = False
                        print("Riders_Q_Heat3")
                    if int(heat_system_female.Q_Heats) > 1 and riders_q_heat_list[3] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_female.Riders_Q_Heat5
                        riders_q_heat_list[3] = False
                        print("Riders_Q_Heat4")
                    if int(heat_system_female.Q_Heats) > 1 and riders_q_heat_list[4] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_female.Riders_Q_Heat6
                        riders_q_heat_list[4] = False
                        print("Riders_Q_Heat5")

            athletes_male = Athlete.objects.filter(category_in_competition=athlete_event.category_in_competition,
                                                   gender='M')
            athletes_male = get_ranking(athletes_male)

            print('Male qtd ' + str(len(athletes_male)))
            print("Generate Male")
            start_position = 0
            heat_count = 0

            if len(athletes_male) > 0:
                heat_system_male = MatrixHeatSystem.objects.get(Riders=len(athletes_male))
                riders_q_heat_list = [True, True,
                                      True, True, True
                    , True]
                print(heat_system_male)
                heat = heat_system_male.Q_Heats
                print('heat ' + str(heat))
                if int(heat_system_male.Q_Heats) > 1:
                    heat_count = heat_system_male.Riders_Q_Heat1
                    heat = 1
                for athlete in athletes_male:
                    start_position += 1
                    leader_board = LeaderBoard()

                    leader_board.athlete = athlete
                    leader_board.username = user
                    leader_board.competition = competition
                    leader_board.ranking = athlete.ranking
                    leader_board.athlete_gender = athlete.gender
                    leader_board.athlete_category_in_competition = athlete.category_in_competition
                    leader_board.Q_Heat_number = heat
                    print('heat ' + str(heat))
                    leader_board.Q_Starting_list = start_position

                    print('start_position ' + str(start_position))
                    print('heat_count ' + str(heat_count))
                    print('heat_system_male.Q_Heats ' + str(heat_system_male.Q_Heats))

                    leader_board.save()
                    if int(heat_system_male.Q_Heats) > 1 and riders_q_heat_list[0] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_male.Riders_Q_Heat2
                        riders_q_heat_list[0] = False
                        print("Riders_Q_Heat1")
                    if int(heat_system_male.Q_Heats) > 1 and riders_q_heat_list[1] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_male.Riders_Q_Heat3
                        riders_q_heat_list[1] = False
                        print("Riders_Q_Heat2")
                    if int(heat_system_male.Q_Heats) > 1 and riders_q_heat_list[2] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_male.Riders_Q_Heat4
                        riders_q_heat_list[2] = False
                        print("Riders_Q_Heat3")
                    if int(heat_system_male.Q_Heats) > 1 and riders_q_heat_list[3] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_male.Riders_Q_Heat5
                        riders_q_heat_list[3] = False
                        print("Riders_Q_Heat4")
                    if int(heat_system_male.Q_Heats) > 1 and riders_q_heat_list[4] and start_position == heat_count:
                        heat += 1
                        start_position = 0
                        heat_count = heat_system_male.Riders_Q_Heat6
                        riders_q_heat_list[4] = False
                        print("Riders_Q_Heat5")

        return {"message": "Heat system generated successfully."}


class LadderSystem(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)
    athlete = AthleteSerializer(many=True, read_only=True)
    competition = CompetitionSerializer(many=True, read_only=True)

    class Meta:
        model = LeaderBoard
        exclude = ['id']

    def create(self, validated_data):
        print("TESTE")
        user = self.context.get("request").user
        competition_id = self.context['request'].data.get('competition_id')
        leaderboard_id = self.context['request'].data.get('leaderboard_id')
        print(competition_id)

        try:
            leaderboard = LeaderBoard.objects.get(id=leaderboard_id)
            print(leaderboard)
        except LeaderBoard.DoesNotExist:
            raise serializers.ValidationError("Leaderboard entry not found")

        return {"message": "Heat system generated successfully."}


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
        print("teste")
        user = self.context.get("request").user
        # Create Competition instance
        competition_data = validated_data.copy()
        events_data = competition_data.pop('events')
        jury_data = competition_data.pop('officials')
        print("1")
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
            print("2")
            athlete_events_data = athlete_data.pop('events')

            for athlete_event_data in athlete_events_data:
                event = Event.objects.get(code=athlete_event_data['code'])
                athlete_data['real_category'] = athlete_event_data['real_category']
                athlete_data['category_in_competition'] = athlete_event_data['category_in_competition']
                Athlete.objects.create(competition=competition, **athlete_data, username=user)
                athlete_events = AthleteEvent.objects.filter(
                    competition=competition,
                    event=event,
                    category_in_competition=athlete_event_data['category_in_competition']
                )
                if not athlete_events.exists():
                    AthleteEvent.objects.create(competition=competition, event=event, **athlete_event_data,
                                                username=user)
                break
            # athlete.events.create(competition=competition, event=event, **athlete_event_data,
            #                          username=user)
            # athlete.events.set(athlete_events)
        return competition


class MatrixHeatSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixHeatSystem
        fields = '__all__'
