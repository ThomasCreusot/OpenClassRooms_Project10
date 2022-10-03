from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from authentication_app.models import User
from authentication_app.serializers import UserSignupSerializer


# https://dev.to/shivamrohilla/user-authentication-in-djangorestframework-using-simplejwt-login
# -signup-3kd8
@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSignupSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            print(data['first_name'])
            user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'],
                username=data['username'], email=data['email'],
                password=make_password(data['password']))
            user.save()
            return Response({'message':'User Created Successfully'},
                status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'User Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
