from rest_framework.serializers import (
    ModelSerializer, 
    EmailField, CharField, 
)
from rest_framework import exceptions

from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserRegisterSerializer(ModelSerializer):
    
    username = CharField(
        style = {'input_type': 'test', 'placeholder': 'Username'}
    )
    email = EmailField(
        required = False,
        style = {'input_type': 'test', 'placeholder': 'Email'}
    )
    password = CharField(
        write_only = True,
        required = True,
        style = {'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = CharField(
        label = 'Password Confirm',
        write_only = True,
        required = True,
        style = {'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user = User.objects.filter(
            Q(username = username) | 
            Q(email = email)
        )
        if user.exists():
            raise exceptions.ValidationError('User is already exists!')

        return data
    
    def validate_password(self, value):
        data = self.get_initial()
        password = data.get('password2')
        password2 = value
        if password2 != password:
            raise exceptions.ValidationError('Password unmatched!')
        return value
    
    def validate_password2(self, value):
        data = self.get_initial()
        password = data.get('password')
        password2 = value
        if password2 != password:
            raise exceptions.ValidationError('Password unmatched!')
        return value

    
    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            username = username,
            email = email
        )
        user.set_password(password)
        user.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):

    username  = CharField(
        style = {'input_type': 'test', 'placeholder': 'Username'}
    )
    password = CharField(
        write_only = True,
        required = True,
        style = {'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):

        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username = username, password = password)
            if user:
                data['user'] = user
            else:
                msg = 'Username or Password is incorrect!'
                raise exceptions.ValidationError(msg)

        return data