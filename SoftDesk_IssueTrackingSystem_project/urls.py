"""SoftDesk_IssueTrackingSystem_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from IssueTracking_app.views import ProjectViewset

import authentication_app.views

router = routers.SimpleRouter()
# nous déclarons une url basée sur le mot clé ‘project’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/project/’
router.register('project', ProjectViewset, basename='project') #paramètre basename  permet de retrouver l’URL complète avec la fonction redirect ; utile pour les tests


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', authentication_app.views.LoginPageView.as_view(), name='login'),
    path('logout/', authentication_app.views.logout_user, name='logout'),
    path('signup/', authentication_app.views.signup_page, name='signup'),


    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),


]
