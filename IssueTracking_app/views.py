#from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet


from IssueTracking_app.models import Project, Issue, Comment, Contributor
from authentication_app.models import User

#from IssueTracking_app.serializers import ProjectSerializer
from IssueTracking_app.serializers import ProjectListSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer, ContributorSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from IssueTracking_app.permissions import ProjectsPermission, IssuesPermission, CommentPermission, ContributorsPermission

from django.db.models import Q


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
    """API endpoint that allows Projects to be CRUD."""

    serializer_class = ProjectListSerializer 
    detail_serializer_class = ProjectDetailSerializer 

    permission_classes = [ProjectsPermission]


    def get_queryset(self):
        #note that with 
        # return Project.objects.filter(author_user_id = self.request.user.id) 
        # http://127.0.0.1:8000/api/projects/1/ 
        # whereas with
        # return Project.objects.all()
        # http://127.0.0.1:8000/api/projects/1/ is  accessible for an Anonym user

        #first version : user access project for which he/she is author 
        # return Project.objects.filter(author_user_id = self.request.user.id)

        #second version : user access project for which he/she is author or contributor
        projects_in_which_user_is_author_or_contributor = Project.objects.filter(
            Q(author_user_id = self.request.user.id) | Q(contributors = self.request.user.id)
        )

        #print("1")
        #print(Project.objects.filter(Q(author_user_id = self.request.user.id)) )
        #print("2")
        #print(Project.objects.filter(Q(contributors = self.request.user.id)))

        #print("3")
        #print(Project.objects.filter(
        #    Q(author_user_id = self.request.user.id) | Q(contributors = self.request.user.id)
        #))

        return projects_in_which_user_is_author_or_contributor
        


    def get_serializer_class(self):
    # cours OC : Si l'action demandée est retrieve nous retournons le serializer de détail
        if self.action == 'retrieve':
            print("a")
            return self.detail_serializer_class
        return super().get_serializer_class() #serializer par defaut







class IssueViewset(ModelViewSet):
    """API endpoint that allows Issues to be CRUD."""

    serializer_class = IssueSerializer 

    permission_classes = [IssuesPermission]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])


class CommentViewset(ModelViewSet):
    """API endpoint that allows Comments to be CRUD."""

    serializer_class = CommentSerializer 

    permission_classes = [CommentPermission]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs['issue_pk'])


class ContributorsViewset(ModelViewSet):
    """API endpoint that allows Contributors to be CRUD."""

    #  Displays contributors objects : a relation betwen a project and a user
    serializer_class = ContributorSerializer 

    permission_classes = [ContributorsPermission]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])


    #  Displays users who got an ID which is in the list of contributors objects
    #serializer_class = ContributorUserSerializer 

    #def get_queryset(self):
    #    id_of_project_in_url = self.kwargs['project_pk']
    #    contributors_queryset = Contributor.objects.filter(project_id=id_of_project_in_url) 
    #    contributors_user_queryset = User.objects.filter(id__in=contributors_queryset) # avec du recul: étange. il me semble que ca marchait, mais ne devrait il pas y avoir une étape supplémentaire ou on cherche un ide dans une liste... d'ids ^^
    #    return contributors_user_queryset
