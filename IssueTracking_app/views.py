#from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

 
from IssueTracking_app.models import Project
from IssueTracking_app.serializers import ProjectSerializer



class ProjectViewset(ModelViewSet):
 
    serializer_class = ProjectSerializer 

    def get_queryset(self):
        return Project.objects.all()
