#from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

 
from IssueTracking_app.models import Project, Issue, Comment, Contributor
#from authentication_app.models import User

#from IssueTracking_app.serializers import ProjectSerializer
from IssueTracking_app.serializers import ProjectListSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer, ContributorSerializer


#original version: no difference between list and detail
#class ProjectViewset(ModelViewSet):
# 
#    serializer_class = ProjectSerializer 
#
#    def get_queryset(self):
#        #print(request.user)
#        #return Project.objects.all()
#        return Project.objects.filter(author_user_id = self.request.user)

#test pour user par defaut


class ProjectViewset(ModelViewSet):
    """
    API endpoint that allows projects to be CRUD.
    """
    serializer_class = ProjectListSerializer 
    detail_serializer_class = ProjectDetailSerializer 

    def get_queryset(self):
        return Project.objects.filter(author_user_id = self.request.user)

    def get_serializer_class(self):
    # cours OC : Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class() #serializer par defaut


class IssueViewset(ModelViewSet):

    serializer_class = IssueSerializer 

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer 

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])


class ContributorsViewset(ModelViewSet):

    serializer_class = ContributorSerializer 

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])

