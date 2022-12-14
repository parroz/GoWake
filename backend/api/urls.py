from django.urls import path
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (CompetitionsAPIView,
                    CompetitionAPIView,
                    EventsAPIView,
                    EventAPIView,
                    OfficialsAPIView,
                    OfficialAPIView,
                    AthletesAPIView, AthleteAPIView, AthleteEventAPIView, AthleteEventsAPIView

 )
"""
router = routers.DefaultRouter()
router.register('competitions',CompetitionViewSet, basename="competitions")
router.register(r'upload', UploadViewSet, basename="upload")
# from .views import api_home
"""

urlpatterns = [
    path('auth/', obtain_auth_token, name='api_auth'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    #path('', api_home.as_view()), # localhost:8000/api/
    path('competitions/', CompetitionsAPIView.as_view(), name='competitions'),
    path('competitions/<int:pk>/', CompetitionAPIView.as_view(), name='competition'),
    path('competitions/<int:competition_pk>/events/', EventsAPIView.as_view(), name='competition_events'),
    path('competitions/<int:competition_pk>/event/<int:event_pk>/', EventAPIView.as_view(), name='competition_event'),
    path('competitions/<int:competition_pk>/officials/', OfficialsAPIView.as_view(), name='competition_officials'),
    path('competitions/<int:competition_pk>/official/<int:official_pk>/', OfficialAPIView.as_view(), name='competition_official'),
    path('competitions/<int:competition_pk>/athletes/', AthletesAPIView.as_view(), name='competition_athletes'),
    path('competitions/<int:competition_pk>/athlete/<int:athlete_pk>/', AthleteAPIView.as_view(), name='competition_athlete'),
    path('competitions/<int:competition_pk>/athlete/<int:athlete_pk>/athlete-events/', AthleteEventsAPIView.as_view(),name='competition_athlete_events'),
    path('competitions/<int:competition_pk>/athlete/<int:athlete_pk>/athlete-event/<int:athlete_event_pk>', AthleteEventAPIView.as_view(),
    name='competition_athlete_event'),
    # path('products/', include('products.urls'))
]
