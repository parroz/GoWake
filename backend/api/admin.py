from django.contrib import admin

from .models import Competition, Categorie, Event, Official, Athlete, AthleteEvent, MatrixHeatSystem, EventDescription, \
    LeaderBoard

admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Official)
admin.site.register(Athlete)
admin.site.register(AthleteEvent)
admin.site.register(MatrixHeatSystem)
admin.site.register(EventDescription)

admin.site.register(Categorie)


class LeaderBoardAdmin(admin.ModelAdmin):
    list_display = ('id','athlete', 'athlete_category_in_competition','round', 'Q_Heat_number',
                    'Q_Starting_list', 'ranking', 'Q_global_pontuation', 'Q_placement',
                      'global_pontuation')


admin.site.register(LeaderBoard, LeaderBoardAdmin)
