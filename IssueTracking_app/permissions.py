from rest_framework.permissions import BasePermission

from IssueTracking_app.models import Contributor
from authentication_app.models import User

from django.db.models import Q


class ProjectCollaboratorssPermission(BasePermission):

    def has_permission(self, request, view):

        #SOLUTION A
        #id_of_project_in_url = view.kwargs['project_pk']

        # queryset of contributors objects, which got a project_id == to the id_of_project_in_url
        #contributors_queryset = Contributor.objects.filter(project_id=id_of_project_in_url) 

        # we got a queryset of contributors which are relations project-user
        # autorisation if False by defaul and become True only if a contributor object (of our
        # queryset) has the id of the authenticated user in its user_id field

        #autorisation = False

        #for contributor in contributors_queryset:
        #    print("contributor.user_id", contributor.user_id)
        #    print("request.user", request.user)
        #    if contributor.user_id == request.user:
        #        autorisation = True

        #SOLUTION B
        id_of_project_in_url = view.kwargs['project_pk']
        urlProject_and_RequestUser_contributor = Contributor.objects.filter(
            Q(project_id=id_of_project_in_url) & Q(user_id=request.user)
            ) 
        print("urlProject_and_RequestUser_contributor", urlProject_and_RequestUser_contributor)

        #SOLUTION A
        #return bool(request.user and request.user.is_authenticated and autorisation == True)
        #SOLUTION B
        return bool(request.user and request.user.is_authenticated and urlProject_and_RequestUser_contributor)
