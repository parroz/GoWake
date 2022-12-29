from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Competition, Official, Athlete, Event, AthleteEvent
from rest_framework.serializers import Serializer, FileField

User = get_user_model()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'id_competition',
            'rounds',
            'event_class',
            'name',
            'createAt',
            'updateAt',
            'username'
        )


class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Official
        fields = (
            'id',
            'id_competition',
            'iwwf_id',
            'position',
            'first_name',
            'last_name',
            'qualification',
            'country',
            'region',
            'createAt',
            'updateAt',
            'username'
        )


class AthleteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteEvent
        fields = (
            'id',
            'id_athlete',
            'name',
            'division',
            'entry_type',
            'participation',
            'real_category',
            'category_in_competition',
            'createAt',
            'updateAt',
            'username'
        )


class AthleteSerializer(serializers.ModelSerializer):
    athlete_events = AthleteEventSerializer(many=True, read_only=True)

    class Meta:
        model = Athlete
        fields = (
            'id',
            'id_competition',
            'fed_id',
            'first_name',
            'last_name',
            'country',
            'gender',
            'year_of_birth',
            'athlete_events',
            'createAt',
            'updateAt',
            'username'
        )


class CompetitionSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    officials = OfficialSerializer(many=True, read_only=True)
    athletes = AthleteSerializer(many=True, read_only=True)

    class Meta:
        model = Competition
        fields = (
            'id',
            'code',
            'discipline',
            'name',
            'age_groups',
            'organizing_country',
            'tournament_type',
            'venue',
            'site_code',
            'beginning_date',
            'events',
            'officials',
            'athletes',
            'end_date',
            'createAt',
            'updateAt',
            'username'
        )


"""
class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    this_is_not_real = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)
"""
# class Meta:
#     model = User
#     fields = [
#         'username',
#         'this_is_not_real',
#         'id'
#     ]

# def get_other_products(self, obj):
#     user = obj
#     my_products_qs = user.product_set.all()[:5]
#     return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data
