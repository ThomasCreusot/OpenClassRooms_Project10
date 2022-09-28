from rest_framework.permissions import BasePermission
from rest_framework import permissions

from IssueTracking_app.models import Contributor, Project, Issue, Comment 
from authentication_app.models import User

from django.shortcuts import get_object_or_404
from django.db.models import Q


"""
Redaction of a permission for each view
For each permission : 
    overwritting the method has_permission
        the if ... safemethods: corresponds to users who ask to view all objects of a model (e.g. : http://127.0.0.1:8000/api/projects/)
        the else: corresponds to the users who ask to update/delete all objects of a model (http://127.0.0.1:8000/api/projects/)

    overwritting the method has_permission
        the if ... safemethods: corresponds to users who ask to view a given object of a model (e.g. : http://127.0.0.1:8000/api/projects/18)
        the else: corresponds to the users who ask to update/delete a given object of a model (http://127.0.0.1:8000/api/projects/18)

Note: 
https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
"""


def give_access_to_():
    return True




class ProjectsPermission(BasePermission):
    """Gives permission :
    -ask to view all Projects      : all authentificated user can ask to view the projects they are inplied in (see filter in view) ; GET in has_permission
    -ask to create all Projects    : all authentificated user can ask to create a project ; POST in has_permission
    -ask to update all Projects    : PUT on http://127.0.0.1:8000/api/projects/ : does not exist ; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
    -ask to delete all Projects    : DELETE on http://127.0.0.1:8000/api/projects/ : does not exist; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)


    -ask to view a given Project   : contributors of a project can ask to view details of the projects ; GET in has_object_permission
    -ask to create a given Project : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/projects/22
    -ask to update a given Project : project author only ; PUT in has_object_permission
    -ask to delete a given Project : project author only ; DELETE in has_object_permission
    """

    message = 'write an adequate message here : permissions.py aaa'

    def has_object_permission(self, request, view, obj):
        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
        if request.method in permissions.SAFE_METHODS:        

            #here: pk and note project_pk : see the router design
            id_of_project_in_url = view.kwargs['pk']
            urlProject_and_RequestUser_contributor = Contributor.objects.filter(
                Q(project_id=id_of_project_in_url) & Q(user_id=request.user)
                ) 
            return bool(request.user and request.user.is_authenticated and urlProject_and_RequestUser_contributor)


        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is other than 'GET', 'OPTIONS' or 'HEAD'.
        else:
            if request.method == "POST":
                return False

            else: # : request.method == "PUT" or request.method == "DELETE":
                #Code in both has_permission and has_object_permission
                id_of_project_in_url = view.kwargs['pk']
                project_object = get_object_or_404(Project, pk=id_of_project_in_url)
                print(project_object.author_user_id == request.user)
                return bool(request.user and request.user.is_authenticated and project_object.author_user_id == request.user)


    def has_permission(self, request, view):
        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
        if request.method in permissions.SAFE_METHODS:        
            return bool(request.user and request.user.is_authenticated)

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is other than 'GET', 'OPTIONS' or 'HEAD'.
        else:
            if request.method == "POST":
                return bool(request.user and request.user.is_authenticated)

            else: # : request.method == "PUT" or request.method == "DELETE":
                #here: pk and note project_pk : see the router design
                #Code in both has_permission and has_object_permission
                id_of_project_in_url = view.kwargs['pk']
                project_object = get_object_or_404(Project, pk=id_of_project_in_url)
                print(project_object.author_user_id == request.user)
                return bool(request.user and request.user.is_authenticated and project_object.author_user_id == request.user)



class CommentPermission(BasePermission):
    """Gives permission to ... of a project (the one in the url) to access ... and ... """

    message = 'write an adequate message here : permissions.py'

    def has_permission(self, request, view):

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
        if request.method in permissions.SAFE_METHODS:        

            return bool(request.user and request.user.is_authenticated and True )

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is other than 'GET', 'OPTIONS' or 'HEAD'.
        else:

            return bool(request.user and request.user.is_authenticated and True )


class ContributorsPermission(BasePermission):
    #//!!\\ !!! role is to allow or not access to creation of contributors which are objects linking projects and users
    # role is not to give or not access to contributors

    """Gives permission to ... of a project (the one in the url) to access ... and ... """

    message = 'write an adequate message here : permissions.py'

    def has_permission(self, request, view):

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
        if request.method in permissions.SAFE_METHODS:        

            return bool(request.user and request.user.is_authenticated and True )

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is other than 'GET', 'OPTIONS' or 'HEAD'.
        else:

            return bool(request.user and request.user.is_authenticated and True )


class IssuesPermission(BasePermission):
    """Gives permission to collaborators of a project (the one in the url) to access issues and ... """

    message = 'You do not have permission to perform this action as you are not a ... of the project'

    def has_permission(self, request, view):

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
        if request.method in permissions.SAFE_METHODS:
        


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
            #print("urlProject_and_RequestUser_contributor", urlProject_and_RequestUser_contributor)

            #SOLUTION A
            #return bool(request.user and request.user.is_authenticated and autorisation == True)
            #SOLUTION B : autorisation only if urlProject_and_RequestUser_contributor not empty
            return bool(request.user and request.user.is_authenticated and urlProject_and_RequestUser_contributor)

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is other than 'GET', 'OPTIONS' or 'HEAD'.
        else:
            return(False)
