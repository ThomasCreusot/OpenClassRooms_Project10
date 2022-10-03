from django.db.models import Q

from rest_framework.viewsets import ModelViewSet

from IssueTracking_app.models import Project, Issue, Comment, Contributor
from IssueTracking_app.serializers import ProjectListSerializer, ProjectDetailSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from IssueTracking_app.permissions import ProjectsPermission, IssuesPermission, CommentPermission, ContributorsPermission


# original version: no difference between list and detail
#class ProjectViewset(ModelViewSet):
# 
#    serializer_class = ProjectSerializer 
#
#    def get_queryset(self):
#        #print(request.user)
#        #return Project.objects.all()
#        return Project.objects.filter(author_user_id = self.request.user)


class ProjectViewset(ModelViewSet):
    """API endpoint that allows Projects to be CRUD."""

    serializer_class = ProjectListSerializer 
    detail_serializer_class = ProjectDetailSerializer 

    permission_classes = [ProjectsPermission]


    def get_queryset(self):
        projects_in_which_user_is_author_or_contributor = Project.objects.filter(
            Q(author_user_id = self.request.user.id) | Q(contributors = self.request.user.id)
        )
        return projects_in_which_user_is_author_or_contributor


    def get_serializer_class(self):
    # OC courses: if the action is 'retrieve', the defaut serializer is returned 
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

    serializer_class = ContributorSerializer

    permission_classes = [ContributorsPermission]

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs['project_pk'])
