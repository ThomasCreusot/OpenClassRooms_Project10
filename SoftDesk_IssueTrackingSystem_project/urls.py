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

# before https://pypi.org/project/drf-nested-routers/
# from rest_framework import routers
from rest_framework_nested import routers

from IssueTracking_app.views import ProjectViewset, IssueViewset, CommentViewset, ContributorsViewset
import authentication_app.views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# nous déclarons une url basée sur le mot clé ‘projects’ et notre view; cela 
# afin que l’url générée soit celle que nous souhaitons ‘/api/projects/’
# 2 arguments : prefix (projects) et viewset class ProjectViewset ; forcément VIEW sous forme de 
# CLASS 
# paramètre basename  permet de retrouver l’URL complète avec la fonction redirect ; utile pour les
# tests
router = routers.SimpleRouter()
router.register('projects', ProjectViewset, basename='projects') 

#https://pypi.org/project/drf-nested-routers/
#ici je suppose que je fais le lien avec un autre rooter, celui de projects ; à l'air de fonctionner
projects_issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_issues_router.register('issues', IssueViewset, basename='project-issues')
# 'basename' is optional. Needed only if the same viewset is registered more than once
# Official DRF docs on this option: http://www.django-rest-framework.org/api-guide/routers/


projects_issues_comments_router = routers.NestedSimpleRouter(projects_issues_router, 'issues', lookup='issue')
projects_issues_comments_router.register('comments', CommentViewset, basename='project-issue-comments')


projects_contributors_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_contributors_router.register('contributors', ContributorsViewset, basename='project-contributors')



urlpatterns = [
    path('admin/', admin.site.urls),

    path('', authentication_app.views.LoginPageView.as_view(), name='login'),
    path('logout/', authentication_app.views.logout_user, name='logout'),
    path('signup/', authentication_app.views.signup_page, name='signup'),


    path('api-auth/', include('rest_framework.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('api/', include(router.urls)),
    path('api/', include(projects_issues_router.urls)),
    path('api/', include(projects_issues_comments_router.urls)),

    path('api/', include(projects_contributors_router.urls)),

]

