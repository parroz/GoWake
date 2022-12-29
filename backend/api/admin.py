from django.contrib import admin

from .models import Competition, Event, Official, Athlete, AthleteEvent


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('code', 'discipline', 'name', 'organizing_country', 'tournament_type', 'venue', 'site_code'
                    , 'beginning_date', 'end_date', 'createAt', 'updateAt', 'username')


@admin.register(Event)
class OfficialAdmin(admin.ModelAdmin):
    list_display = ('id_competition', 'rounds', 'event_class', 'name', 'createAt', 'updateAt', 'username')


@admin.register(Official)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id_competition', 'position', 'first_name', 'last_name', 'qualification', 'country',
                    'region', 'createAt', 'updateAt', 'username')


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('id_competition', 'fed_id', 'first_name', 'last_name', 'country',
                    'gender', 'year_of_birth', 'createAt', 'updateAt', 'username')


@admin.register(AthleteEvent)
class AthleteEventAdmin(admin.ModelAdmin):
    list_display = ('id_athlete', 'name', 'division', 'entry_type', 'participation', 'real_category',
                    'category_in_competition', 'createAt', 'updateAt', 'username')
