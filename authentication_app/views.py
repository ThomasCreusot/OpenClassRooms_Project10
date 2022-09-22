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


