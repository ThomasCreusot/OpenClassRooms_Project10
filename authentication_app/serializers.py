from rest_framework import serializers
from authentication_app.models import User


#https://dev.to/shivamrohilla/user-authentication-in-djangorestframework-using-simplejwt-login-signup-3kd8
class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    extra_kwargs = {
        'first_name': {'required': True, 'allow_blank': False},
        'last_name': {'required': True, 'allow_blank': False},
        'email': {'required': True, 'allow_blank': False},
        'password': {'required': True, 'allow_blank': False},        
    }    

#https://dev.to/shivamrohilla/user-authentication-in-djangorestframework-using-simplejwt-login-signup-3kd8
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')
