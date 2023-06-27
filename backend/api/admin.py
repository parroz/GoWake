from django.contrib import admin

from .models import Competition, Categorie, Event, Official, Athlete, AthleteEvent, MatrixHeatSystem, \
    LeaderBoard

admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Official)

admin.site.register(AthleteEvent)
admin.site.register(MatrixHeatSystem)

admin.site.register(Categorie)


class AthleteAdmin(admin.ModelAdmin):
    list_display = ('id', 'fed_id', 'first_name', 'last_name', 'country',
                    'gender', 'year_of_birth', 'ranking', 'real_category',
                    'category_in_competition')


admin.site.register(Athlete,AthleteAdmin)


class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'athlete', 'athlete_category_in_competition', 'round', 'Q_Heat_number',
                    'Q_Starting_list', 'ranking', 'Q_global_pontuation', 'Q_placement',
                    'global_pontuation', 'ranking_event_final_points')


admin.site.register(LeaderBoard, LeaderBoardAdmin)
