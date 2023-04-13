from django.db import models
from django.contrib.auth.models import User


class Base(models.Model):
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

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
    competition = models.ForeignKey(Competition, related_name='events', on_delete=models.CASCADE)
    rounds = models.IntegerField()
    event_class = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    code = models.CharField(blank=True, max_length=100)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.name


class Official(Base):
    competition = models.ForeignKey(Competition, related_name='officials', on_delete=models.CASCADE)
    iwwfid = models.CharField(max_length=10)
    position = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=10)
    region = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Official'
        verbose_name_plural = 'Officials'

    def __str__(self):
        return self.iwwfid + " - " + self.first_name + " " + self.last_name


class AthleteEvent(Base):
    competition = models.ForeignKey(Competition, related_name='athlete_events', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='event_detail', on_delete=models.CASCADE)
    division = models.CharField(max_length=20, blank=True)
    entry_type = models.CharField(max_length=10, blank=True)
    participation = models.BooleanField(default=True, blank=True)
    real_category = models.CharField(max_length=5, blank=True)
    category_in_competition = models.CharField(max_length=10, blank=True)
    code = models.CharField(blank=True, max_length=100)

    class Meta:
        verbose_name = 'AthleteEvent'
        verbose_name_plural = 'AthleteEvents'

    def __str__(self):
        return self.real_category + " - " + self.event.name


class Athlete(Base):
    competition = models.ForeignKey(Competition, related_name='athletes', on_delete=models.CASCADE)
    fed_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    year_of_birth = models.IntegerField()
    events = models.ManyToManyField(AthleteEvent, related_name='events')

    class Meta:
        verbose_name = 'Athlete'
        verbose_name_plural = 'Athletes'

    def __str__(self):
        return self.first_name + " " + self.last_name


class MatrixHeatSystem(models.Model):
    Riders = models.CharField(max_length=5, blank=True)
    Q_Heats = models.CharField(max_length=5, blank=True)
    LCQ_Heats = models.CharField(max_length=20, blank=True)
    QrtFinal_Heats = models.CharField(max_length=20, blank=True)
    SemiFinal_Heats = models.CharField(max_length=20, blank=True)
    Final_Heats = models.CharField(max_length=20, blank=True)

    Riders_Q_Heat1 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_Q_Heat1 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_Q_Heat1 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_Q_Heat1 = models.CharField(max_length=20, blank=True)
    RemainingRidersToLCQ_Q_Heat1 = models.CharField(max_length=20, blank=True)

    Riders_Q_Heat2 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_Q_Heat2 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_Q_Heat2 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_Q_Heat2 = models.CharField(max_length=20, blank=True)
    RemainingRidersToLCQ_Q_Heat2 = models.CharField(max_length=20, blank=True)

    Riders_Q_Heat3 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_Q_Heat3 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_Q_Heat3 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_Q_Heat3 = models.CharField(max_length=20, blank=True)
    RemainingRidersToLCQ_Q_Heat3 = models.CharField(max_length=20, blank=True)

    Riders_Q_Heat4 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_Q_Heat4 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_Q_Heat4 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_Q_Heat4 = models.CharField(max_length=20, blank=True)
    RemainingRidersToLCQ_Q_Heat4 = models.CharField(max_length=20, blank=True)

    Riders_Q_Heat5 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_Q_Heat5 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_Q_Heat5 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_Q_Heat5 = models.CharField(max_length=20, blank=True)
    RemainingRidersToLCQ_Q_Heat5 = models.CharField(max_length=20, blank=True)

    Riders_Q_Heat6 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_Q_Heat6 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_Q_Heat6 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_Q_Heat6 = models.CharField(max_length=20, blank=True)
    RemainingRidersToLCQ_Q_Heat6 = models.CharField(max_length=20, blank=True)

    Riders_LCQ_Heat1 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_LCQ_Heat1 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_LCQ_Heat1 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_LCQ_Heat1 = models.CharField(max_length=20, blank=True)

    Riders_LCQ_Heat2 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_LCQ_Heat2 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_LCQ_Heat2 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_LCQ_Heat2 = models.CharField(max_length=20, blank=True)

    Riders_LCQ_Heat3 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_LCQ_Heat3 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_LCQ_Heat3 = models.CharField(max_length=20, blank=True)
    TopRidersToQrtFinal_LCQ_Heat3 = models.CharField(max_length=20, blank=True)

    Riders_QrtFinal_Heat1 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_QrtFinal_Heat1 = models.CharField(max_length=5, blank=True)

    Riders_QrtFinal_Heat2 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_QrtFinal_Heat2 = models.CharField(max_length=5, blank=True)

    Riders_QrtFinal_Heat3 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_QrtFinal_Heat3 = models.CharField(max_length=5, blank=True)

    Riders_QrtFinal_Heat4 = models.CharField(max_length=5, blank=True)
    TopRidersToSemiFinal_QrtFinal_Heat4 = models.CharField(max_length=5, blank=True)

    Riders_SemiFinal_Heat1 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_SemiFinal_Heat1 = models.CharField(max_length=5, blank=True)

    Riders_SemiFinal_Heat2 = models.CharField(max_length=5, blank=True)
    TopRidersToFinal_SemiFinal_Heat2 = models.CharField(max_length=5, blank=True)

    Riders_Final_Heat1 = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return "Rider: " + self.Riders


class LeaderBoard(models.Model):
    athlete = models.ForeignKey(Athlete, related_name='athletes_leaderboards',on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='competition_leaderboards', on_delete=models.CASCADE)
    events = models.ManyToManyField(AthleteEvent, related_name='events_leaderboard')

    Q_Heat_number = models.CharField(max_length=5, blank=True)
    Q_Starting_list = models.CharField(max_length=5, blank=True)
    Q_1st_Judge_Last_name = models.CharField(max_length=5, blank=True)
    Q_1st_judge_first_name = models.CharField(max_length=5, blank=True)
    Q_1st_judge_iwwf_id = models.CharField(max_length=5, blank=True)
    Q_2nd_Judge_Last_name = models.CharField(max_length=5, blank=True)
    Q_2nd_judge_first_name = models.CharField(max_length=5, blank=True)
    Q_2nd_judge_iwwf_id = models.CharField(max_length=5, blank=True)
    Q_3rd_Judge_Last_name = models.CharField(max_length=5, blank=True)
    Q_3rd_judge_first_name = models.CharField(max_length=5, blank=True)
    Q_3rd_judge_iwwf_id = models.CharField(max_length=5, blank=True)
    Q_1st_judge_atlhete_front_foot = models.CharField(max_length=5, blank=True)
    Q_2nd_judge_atlhete_front_foot = models.CharField(max_length=5, blank=True)
    Q_3rd_judge_atlhete_front_foot = models.CharField(max_length=5, blank=True)
    Q_1st_judge_Intensity_score = models.CharField(max_length=5, blank=True)
    Q_2nd_judge_Intensity_score = models.CharField(max_length=5, blank=True)
    Q_3rd_judge_Intensity_score = models.CharField(max_length=5, blank=True)
    Q_1st_judge_Execution_score = models.CharField(max_length=5, blank=True)
    Q_2nd_judge_Execution_score = models.CharField(max_length=5, blank=True)
    Q_2nd_judge_Execution_score = models.CharField(max_length=5, blank=True)