from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.models import Group
from ..models import JuryCode


class RegistrationJurySerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    print('RegistrationJurySerializer')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        print(self.validated_data)
        password = self.validated_data['password']
        password2 = self.validated_data['password']

        if password != password2:
            raise serializers.ValidationError({'error': 'Password1 e Password2 should be the same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exist!'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("This field may not be blank.")
        else:
            return value

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password']

        if password != password2:
            raise serializers.ValidationError({'error': 'Password1 e Password2 should be the same!'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exist!'})

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account


class JuryCodeSerializer(serializers.ModelSerializer):
    username = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = JuryCode
        fields = '__all__'
