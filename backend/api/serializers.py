import random
import itertools
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .auxiliar_functions import process_leaderboards_3_6, process_leaderboards_7_10, process_leaderboards_11_12, \
    process_leaderboards_7_10_LCQ, process_leaderboards_11_12_LCQ, set_ranking_pontuation
from .models import Competition, Official, Athlete, Event, AthleteEvent, MatrixHeatSystem, LeaderBoard, Categorie
from rest_framework.serializers import Serializer, FileField
from rest_framework.fields import CurrentUserDefault
from django.db.models import Count

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


class LeaderboardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaderBoard
        fields = ['round', 'athlete_category_in_competition', 'athlete_gender', 'Q_Heat_number']


class CompetitionAppSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)
    leaderboards = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        exclude = ['createAt', 'updateAt']

    def get_leaderboards(self, instance):
        queryset = LeaderBoard.objects.filter(competition=instance) \
            .values('athlete_category_in_competition', 'athlete_gender', 'round', 'Q_Heat_number') \
            .annotate(athlete_category_in_competition_count=Count('*'))

        leaderboard_serializer = LeaderboardCategorySerializer(queryset, many=True)
        return leaderboard_serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['leaderboards'] = self.get_leaderboards(instance)
        return representation


def get_ranking(athletes):
    rankings = list(range(1, 999 + 1))
    random.shuffle(rankings)
    for i, athlete in enumerate(athletes):
        athlete.ranking = rankings[i]
        real_category = Categorie.objects.filter(description=athlete.real_category).first()
        category_in_competition = Categorie.objects.filter(description=athlete.category_in_competition).first()
        if real_category.code < category_in_competition.code:
            athlete.ranking = athlete.ranking * 0.75
        athlete.save()

    return athletes.order_by('-ranking')


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

            if len(athletes_female) > 0:
                heat_system_female = MatrixHeatSystem.objects.get(Riders=len(athletes_female))
                print(heat_system_female)
                riders_start_positions = [0, 0, 0, 0, 0, 0]
                riders_start_positions[0] = heat_system_female.Riders_Q_Heat1
                active_heat = 1
                snake_control = 0
                valid_last = False
                if int(heat_system_female.Q_Heats) > 1:
                    if int(heat_system_female.Q_Heats) == 2:
                        riders_start_positions[1] = heat_system_female.Riders_Q_Heat2
                        active_heat = 2
                    if int(heat_system_female.Q_Heats) == 3:
                        riders_start_positions[1] = heat_system_female.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_female.Riders_Q_Heat3
                        active_heat = 3
                    if int(heat_system_female.Q_Heats) == 4:
                        riders_start_positions[1] = heat_system_female.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_female.Riders_Q_Heat3
                        riders_start_positions[3] = heat_system_female.Riders_Q_Heat4
                        active_heat = 4
                    if int(heat_system_female.Q_Heats) == 5:
                        riders_start_positions[1] = heat_system_female.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_female.Riders_Q_Heat3
                        riders_start_positions[3] = heat_system_female.Riders_Q_Heat4
                        riders_start_positions[4] = heat_system_female.Riders_Q_Heat5
                        active_heat = 5
                    if int(heat_system_female.Q_Heats) == 6:
                        riders_start_positions[1] = heat_system_female.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_female.Riders_Q_Heat3
                        riders_start_positions[3] = heat_system_female.Riders_Q_Heat4
                        riders_start_positions[4] = heat_system_female.Riders_Q_Heat5
                        riders_start_positions[5] = heat_system_female.Riders_Q_Heat6
                        active_heat = 6

                for athlete in athletes_female:
                    leader_board = LeaderBoard()
                    leader_board.athlete = athlete
                    leader_board.username = user
                    leader_board.competition = competition
                    leader_board.ranking = athlete.ranking
                    leader_board.athlete_gender = athlete.gender
                    leader_board.athlete_category_in_competition = athlete.category_in_competition
                    leader_board.round = 'QLF'
                    if active_heat == 1:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[0]
                        leader_board.save()
                        riders_start_positions[0] -= 1
                        if snake_control == 1:
                            active_heat = int(heat_system_female.Q_Heats)
                            snake_control = 0
                        else:
                            snake_control += 1
                        continue

                    if active_heat == 2:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[1]
                        leader_board.save()
                        riders_start_positions[1] -= 1

                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_female.Q_Heats) == 2:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 3:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[2]
                        leader_board.save()
                        riders_start_positions[2] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_female.Q_Heats) == 3:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 4:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[3]
                        leader_board.save()
                        riders_start_positions[3] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_female.Q_Heats) == 4:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 5:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[4]
                        leader_board.save()
                        riders_start_positions[4] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_female.Q_Heats) == 5:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 6:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[5]
                        leader_board.save()
                        riders_start_positions[5] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_female.Q_Heats) == 6:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

            athletes_male = Athlete.objects.filter(category_in_competition=athlete_event.category_in_competition,
                                                   gender='M')
            athletes_male = get_ranking(athletes_male)

            if len(athletes_male) > 0:
                heat_system_male = MatrixHeatSystem.objects.get(Riders=len(athletes_male))
                print(heat_system_male)
                riders_start_positions = [0, 0, 0, 0, 0, 0]
                riders_start_positions[0] = heat_system_male.Riders_Q_Heat1
                active_heat = 1
                snake_control = 0
                valid_last = False
                if int(heat_system_male.Q_Heats) > 1:
                    if int(heat_system_male.Q_Heats) == 2:
                        riders_start_positions[1] = heat_system_male.Riders_Q_Heat2
                        active_heat = 2
                    if int(heat_system_male.Q_Heats) == 3:
                        riders_start_positions[1] = heat_system_male.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_male.Riders_Q_Heat3
                        active_heat = 3
                    if int(heat_system_male.Q_Heats) == 4:
                        riders_start_positions[1] = heat_system_male.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_male.Riders_Q_Heat3
                        riders_start_positions[3] = heat_system_male.Riders_Q_Heat4
                        active_heat = 4
                    if int(heat_system_male.Q_Heats) == 5:
                        riders_start_positions[1] = heat_system_male.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_male.Riders_Q_Heat3
                        riders_start_positions[3] = heat_system_male.Riders_Q_Heat4
                        riders_start_positions[4] = heat_system_male.Riders_Q_Heat5
                        active_heat = 5
                    if int(heat_system_male.Q_Heats) == 6:
                        riders_start_positions[1] = heat_system_male.Riders_Q_Heat2
                        riders_start_positions[2] = heat_system_male.Riders_Q_Heat3
                        riders_start_positions[3] = heat_system_male.Riders_Q_Heat4
                        riders_start_positions[4] = heat_system_male.Riders_Q_Heat5
                        riders_start_positions[5] = heat_system_male.Riders_Q_Heat6
                        active_heat = 6
                for athlete in athletes_male:
                    leader_board = LeaderBoard()
                    leader_board.athlete = athlete
                    leader_board.username = user
                    leader_board.competition = competition
                    leader_board.ranking = athlete.ranking
                    leader_board.athlete_gender = athlete.gender
                    leader_board.athlete_category_in_competition = athlete.category_in_competition
                    leader_board.round = 'QLF'

                    if active_heat == 1:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[0]
                        leader_board.save()
                        riders_start_positions[0] -= 1
                        if snake_control == 1:
                            active_heat = int(heat_system_male.Q_Heats)
                            snake_control = 0
                        else:
                            snake_control += 1
                        continue

                    if active_heat == 2:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[1]
                        leader_board.save()
                        riders_start_positions[1] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_male.Q_Heats) == 2:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 3:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[2]
                        leader_board.save()
                        riders_start_positions[2] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_male.Q_Heats) == 3:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 4:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[3]
                        leader_board.save()
                        riders_start_positions[3] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_male.Q_Heats) == 4:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 5:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[4]
                        leader_board.save()
                        riders_start_positions[4] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_male.Q_Heats) == 5:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

                    if active_heat == 6:
                        leader_board.Q_Heat_number = active_heat
                        leader_board.Q_Starting_list = riders_start_positions[5]
                        leader_board.save()
                        riders_start_positions[5] -= 1
                        if snake_control == 1:
                            active_heat -= 1
                            snake_control = 0
                        else:
                            snake_control += 1

                        if not valid_last and int(heat_system_male.Q_Heats) == 6:
                            valid_last = True
                            active_heat -= 1
                            snake_control = 0
                        continue

        return {"message": "Heat system generated successfully."}


def get_round(phase, round):
    if phase == 'QLF' and round == 'final':
        return 'Final'
    elif phase == 'LCQ':
        global_pontuation = '-LCQ_global_pontuation'
    elif phase == 'QrtFinal':
        global_pontuation = '-QrtFinal_global_pontuation'
    elif phase == 'SemiFinal':
        global_pontuation = '-SemiFinal_global_pontuation'
    elif phase == 'Final':
        global_pontuation = '-Final_global_pontuation'

    return global_pontuation


def group_leaderboards(phase, leaderboards):
    grouped_leaderboards = []

    if phase == 'QLF':
        key_attr = 'Q_heat'
    elif phase == 'LCQ':
        key_attr = 'LCQ_Heat_number'
    elif phase == 'QrtFinal':
        key_attr = 'QrtFinal_Heat_number'
    elif phase == 'SemiFinal':
        key_attr = 'SemiFinal_Heat_number'
    elif phase == 'Final':
        key_attr = 'Final_Heat_number'
    else:
        return grouped_leaderboards

    sorted_leaderboards = sorted(leaderboards, key=lambda x: getattr(x, key_attr))

    for key, group in itertools.groupby(sorted_leaderboards, key=lambda x: getattr(x, key_attr)):
        group_list = list(group)
        grouped_leaderboards.extend(group_list)

    return grouped_leaderboards


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
        phase = self.context['request'].data.get('phase')

        try:
            competition = Competition.objects.get(id=competition_id)

        except Competition.DoesNotExist:
            raise serializers.ValidationError("Competition with id={} does not exist".format(competition_id))

        athlete_events = AthleteEvent.objects.filter(competition=competition)

        for athlete_event in athlete_events:
            print(athlete_event)
            athletes_female = Athlete.objects.filter(category_in_competition=athlete_event.category_in_competition,
                                                     gender='F')

            if len(athletes_female) > 0:
                heat_system_female = MatrixHeatSystem.objects.get(Riders=len(athletes_female))

                if phase == 'QLF':
                    if 3 <= heat_system_female.Riders <= 6:
                        process_leaderboards_3_6(phase, competition, 'F', athlete_event, user)
                    if 7 <= heat_system_female.Riders <= 10:
                        process_leaderboards_7_10(phase, competition, 'F', athlete_event, user)
                    if 11 <= heat_system_female.Riders <= 12:
                        process_leaderboards_11_12(phase, competition, 'F', athlete_event, heat_system_female, user)
                if phase == 'LCQ':
                    if 7 <= heat_system_female.Riders <= 10:
                        process_leaderboards_7_10_LCQ(phase, competition, 'F', athlete_event, user)
                    if 11 <= heat_system_female.Riders <= 12:
                        process_leaderboards_11_12_LCQ(phase, competition, 'F', athlete_event, user)
            if phase == 'Final':
                set_ranking_pontuation(competition, 'F', athlete_event, phase)

            athletes_male = Athlete.objects.filter(category_in_competition=athlete_event.category_in_competition,
                                                   gender='M')

            if len(athletes_male) > 0:
                heat_system_male = MatrixHeatSystem.objects.get(Riders=len(athletes_male))
                if phase == 'QLF':
                    if 3 <= heat_system_male.Riders <= 6:
                        process_leaderboards_3_6(phase, competition, 'M', athlete_event, user)
                    if 7 <= heat_system_male.Riders <= 10:
                        process_leaderboards_7_10(phase, competition, 'M', athlete_event, user)
                    if 11 <= heat_system_male.Riders <= 12:
                        process_leaderboards_11_12(phase, competition, 'M', athlete_event, heat_system_male, user)
                if phase == 'LCQ':
                    if 7 <= heat_system_male.Riders <= 10:
                        process_leaderboards_7_10_LCQ(phase, competition, 'M', athlete_event, user)
                    if 11 <= heat_system_male.Riders <= 12:
                        process_leaderboards_11_12_LCQ(phase, competition, 'M', athlete_event, user)
                if phase == 'Final':
                    set_ranking_pontuation(competition, 'M', athlete_event, phase)

        return {"message": "Ladder system generated successfully."}


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
        competition_data = validated_data.copy()
        events_data = competition_data.pop('events')
        jury_data = competition_data.pop('officials')
        athletes_data = competition_data.pop('athletes')
        competition = Competition.objects.create(**competition_data, username=user)

        for event_data in events_data:
            Event.objects.create(competition=competition, **event_data, username=user)

        for official_data in jury_data:
            Official.objects.create(competition=competition, **official_data, username=user)
            official_iwwfid = official_data.get('iwwfid')

        for athlete_data in athletes_data:
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

        return competition


class MatrixHeatSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatrixHeatSystem
        fields = '__all__'
