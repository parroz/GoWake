from django.db import models


class Base(models.Model):
    createAt = models.DateTimeField(auto_now=True)
    updateAt = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255)

    class Meta:
        abstract = True


class Competition(Base):
    code = models.CharField(unique=True, max_length=15)
    discipline = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    organizing_country = models.CharField(max_length=5)
    tournament_type = models.CharField(max_length=10)
    venue = models.CharField(max_length=100)
    site_code = models.CharField(max_length=100)
    age_groups = models.CharField(max_length=20)
    beginning_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)

    class Meta:
        verbose_name = 'Competition'
        verbose_name_plural = 'Competitions'

    def __str__(self):
        return self.code


class Event(Base):
    id_competition = models.ForeignKey(Competition, related_name='events', on_delete=models.CASCADE)
    rounds = models.IntegerField()
    event_class = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'


class Official(Base):
    id_competition = models.ForeignKey(Competition, related_name='officials', on_delete=models.CASCADE)
    iwwf_id = models.CharField(max_length=10)
    position = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=10)
    region = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Official'
        verbose_name_plural = 'Officials'


class Athlete(Base):
    id_competition = models.ForeignKey(Competition, related_name='athletes', on_delete=models.CASCADE)
    fed_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    year_of_birth = models.IntegerField()

    class Meta:
        verbose_name = 'Athlete'
        verbose_name_plural = 'Athletes'


class AthleteEvent(Base):
    id_athlete = models.ForeignKey(Athlete, related_name='athlete_events', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    division = models.CharField(max_length=20, blank=True)
    entry_type = models.CharField(max_length=10)
    participation = models.BooleanField(default=True)
    real_category = models.CharField(max_length=5)
    category_in_competition = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'AthleteEvent'
        verbose_name_plural = 'AthleteEvents'
