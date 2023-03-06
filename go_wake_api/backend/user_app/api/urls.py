from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import registration_view,logout_view, login_view, change_password_view

urlpatterns = [
    path('login/', login_view,name='login'),
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change-password'),
]

