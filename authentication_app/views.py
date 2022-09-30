"""
LoginPageView
logout_user
signup_page
"""

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.conf import settings  # access to LOGIN_REDIRECT_URL

from authentication_app.models import User

from rest_framework.permissions import IsAuthenticated

from authentication_app.serializers import UserSignupSerializer, UserSerializer


class LoginPageView(View):
    """Return an objetHttpResponse corresponding to the login page"""
    
    template_name = 'authentication_app/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                #return redirect('api/project/')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


def logout_user(request):
    """Logs out an user"""

    logout(request)
    return redirect('login')


def signup_page(request):
    """Return an objetHttpResponse corresponding to the sign up page"""

    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication_app/signup.html', context={'form': form})




from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes

#class SignupViewset(ModelViewSet):
#    """API endpoint that allows User to Signup"""
#
#    serializer_class = UserSignupSerializer
#    permission_classes = [AllowAny]
#
#
#    def get_queryset(self):
#        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

#https://dev.to/shivamrohilla/user-authentication-in-djangorestframework-using-simplejwt-login-signup-3kd8

@api_view(['POST'])
def signup(request):
    data = request.data
    serializer = UserSignupSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            print(data['first_name'])
            user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], username=data['username'], email=data['email'], password=make_password(data['password']))
            user.save()
            return Response({'message':'User Created Successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'User Already Exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ANNULé, AU FINAL CE QUE L'ON VEUT CE SONT LES TOKENS
#https://dev.to/shivamrohilla/user-authentication-in-djangorestframework-using-simplejwt-login-signup-3kd8
#@api_view(['GET'])
#def login(request):
#
#    data = request.data
#    if User.objects.filter(username=data['username']).exists():
#        user = User.objects.get(username=data['username'])
#        if user.check_password(data['password']):
#
#            return Response(UserSerializer(instance=user).data, status=status.HTTP_200_OK)
#        else:
#
#            return Response({'message':'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)
#    else:
#
#        return Response({'message':'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)

