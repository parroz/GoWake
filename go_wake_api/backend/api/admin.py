from django.contrib import admin

from .models import Competition, Event, Official, Athlete, AthleteEvent

admin.site.register(Competition)
admin.site.register(Event)
admin.site.register(Official)
admin.site.register(Athlete)
admin.site.register(AthleteEvent)

