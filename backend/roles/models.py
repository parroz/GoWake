from django.db import models
from django_countries.fields import CountryField
from datetime import date
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class OfficialCategory(models.Model):
	name = models.CharField(max_length=200, blank=False, unique=True)

class Region(models.Model):
	name = models.CharField(max_length=200, blank=False, unique=True)

class Official(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	category = models.ManyToManyField(OfficialCategory)
	IWWFId = models.CharField(max_length=200, blank=True)
	country = CountryField(blank=False)
	region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return f'{self.firstname} {self.lastname}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Official.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

# class Category(models.Model):
#     GENDER_MALE = 0
#     GENDER_FEMALE = 1

#     GENDER_CHOICES = [
#         (GENDER_MALE, 'Male'),
#         (GENDER_FEMALE, 'Female'),
#     ]
#     minAge = models.IntegerField(blank=False)
#     maxAge = models.IntegerField(blank=False)
#     name = models.CharField(max_length=200, null=False, blank=False)
#     shortName = models.CharField(max_length=10, null=False, blank=False)
#     description = models.TextField(null=True, blank=True)
#     rank = models.IntegerField(blank=False, default=1)
#     gender = models.IntegerField(choices=GENDER_CHOICES, default=0)

#     def __str__(self):
#         return self.name


# class Athlete(models.Model):
#     GENDER_MALE = 0
#     GENDER_FEMALE = 1

#     GENDER_CHOICES = [
#         (GENDER_MALE, 'Male'),
#         (GENDER_FEMALE, 'Female'),
#     ]

#     IWWFId = models.CharField(max_length=200, blank=False, unique=True)
#     lastname = models.CharField(max_length=200, blank=False, unique=False)
#     firstname = models.CharField(max_length=200, blank=False, unique=False)
#     name = models.CharField(max_length=200, blank=False, unique=False)
#     yearOfBirth = models.IntegerField(null=False)
#     country = CountryField(blank=False)
#     gender = models.IntegerField(choices=GENDER_CHOICES, default=0)

#     ranking_point = models.IntegerField(null=True, blank=True, default=0)


#     def __str__(self):
#         return self.name

#     def age(self):
#         today = date.today()
#         return today.year - self.date_Of_Birth.year - (
#                 (today.month, today.day) < (self.date_Of_Birth.month, se$

#     def category(self):
#         cats = Category.objects.filter(gender=self.gender)
#         for c in cats:
#             if c.minAge <= self.age() and (c.maxAge == 0 or c.maxAge >= $
#                 return c
#         return 0

#     def categories(self):
#         myCats = list()
#         cats = Category.objects.filter(gender=self.gender)
#         myCat = self.category()
#         for c in cats:
#             if myCat.rank <= 0 and c.rank <= 0 and c.rank >= myCat.rank:
#                 myCats.append(c)
#             elif myCat.rank >= 0 and c.rank >= 0 and c.rank <= myCat.ran$
#                 myCats.append(c)

#         return myCats



