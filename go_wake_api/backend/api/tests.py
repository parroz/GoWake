from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from . import models
from django.urls import reverse


class CompetitionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="exemplo", password="novapass@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.Competition.objects.create(code="TESTCODE", discipline="wakeboard",
                                                        name="Campeonato Franca", organizing_country="PT",
                                                        tournament_type="NatcCH", venue="Paris",
                                                        site_code="FRPARIS", age_groups="IWWF",
                                                        beginning_date="2023-10-01 18:04:31",
                                                        end_date="2023-12-23 18:04:31", username=self.user)

    def test_competition_create(self):
        data = {
            "code": "TESTCODE",
            "discipline": "wakeboard",
            "name": "Campeonato Franca",
            "organizing_country": "PT",
            "tournament_type": "NatcCH",
            "venue": "Paris",
            "site_code": "FRPARIS",
            "age_groups": "IWWF",
            "beginning_date": "2023-10-01 18:04:31",
            "end_date": "2023-12-23 18:04:31",
            "username": self.user
        }
        response = self.client.post(reverse('competition-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_competition_list(self):
        response = self.client.get(reverse('competitions'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_competition_ind(self):
        response = self.client.get(reverse('competition', args=(self.stream.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
