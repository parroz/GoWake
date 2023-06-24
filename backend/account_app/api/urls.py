from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view,name='login'),
    path('login-app/', login_app_view,name='login-app'),
    path('register/', registration_view, name='register'),
    path('register-jury/', register_jury_view, name='register-jury'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change-password'),
]

