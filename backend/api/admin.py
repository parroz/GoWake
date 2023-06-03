from django.contrib import admin

from .models import Competition,Categorie, Event, Official, Athlete, AthleteEvent, MatrixHeatSystem, EventDescription,LeaderBoard

admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Official)
admin.site.register(Athlete)
admin.site.register(AthleteEvent)
admin.site.register(MatrixHeatSystem)
admin.site.register(EventDescription)
admin.site.register(LeaderBoard)
admin.site.register(Categorie)

