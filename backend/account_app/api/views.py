from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import RegistrationSerializer, RegistrationJurySerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from ..models import receiver, create_auth_token, JuryCode
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register_jury_view(request):
    print('register_jury_view')
    if request.method == 'POST':
        serializer = RegistrationJurySerializer(data=request.data)
        data = {}
        if not JuryCode.objects.filter(code=request.data['code']).exists():
            return Response({"error": "The entered code " + request.data['code'] + " does not exist!"}, status=400)

        if serializer.is_valid():
            account = serializer.save()
            group = Group.objects.get(name=request.data['group'])
            group.user_set.add(account)
            data['response'] = "Registration Sucessful!"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            print('update jury code')

            user = User.objects.get(username=account.username)
            if JuryCode.objects.filter(code=request.data['code'], username=user).exists():
                return Response({"error": "The entered code and username already associate!"}, status=400)
            print('register_jury_view 2')
            jury_code = JuryCode.objects.get(code=request.data['code'])
            jury_code.username = user
            jury_code.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Sucessful!"
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_app_view(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        juryCode = JuryCode.objects.filter(username=user).first()

        if user:
            response_data = {
                "token": user.auth_token.key,
                "email": user.email,
                "username": user.username,
                "role": user.groups.first().name if user.groups.all() else "None"
            }

            if juryCode:
                response_data["juryCode"] = juryCode.code

            return Response(response_data)
        else:
            return Response({"error": "Wrong Credentials"}, status=400)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        if user:
            return Response(
                {"token": user.auth_token.key, "email": user.email, "username": user.username,
                 "role": user.groups.first().name if user.groups.all() else "None"})
        else:
            return Response({"error": "Wrong Credentials"}, status=400)


@api_view(['PUT'])
def change_password_view(request):
    permission_classes = (IsAuthenticated,)
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    if not user.check_password(current_password):
        return Response({'current_password': ['Wrong password.']},
                        status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new_password)
    user.save()
    return Response({'detail': 'Password updated successfully.'},
                    status=status.HTTP_200_OK)
