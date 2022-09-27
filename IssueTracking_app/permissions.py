from rest_framework.permissions import BasePermission

from IssueTracking_app.models import Contributor, Project
from authentication_app.models import User

from django.db.models import Q

from rest_framework import permissions

from django.shortcuts import get_object_or_404

"""Pour s'y retrouver : 
pour chaque vue j'écris une permission
pour chaque permission : on surcharge la méthode has_permission
dans le if ... safemethods : les lecteurs
dans le else: ceux qui mettent à jour, suppriment

la question : le create ? comment le différencier du update
avec un if imbriqué : if request.method == "POST"
"""

class ProjectsPermission(BasePermission):
    """Gives permission 
    -to all contributors of the project read the project with GET : filter in views. with GET
    -to anyone to create a project with POST
    -to project author (only) to update or delete a project with PUT or DELETE
    """

    message = 'write an adequate message here : permissions.py'

    def has_permission(self, request, view):

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is 'GET', 'OPTIONS' or 'HEAD'.
        # to all authentificated user to ask a list of the projects they are inplied in (see filter in view) ; with GET
        if request.method in permissions.SAFE_METHODS:        
            return bool(request.user and request.user.is_authenticated)

        # https://www.django-rest-framework.org/api-guide/permissions/ : if method is other than 'GET', 'OPTIONS' or 'HEAD'.
        else:
            # to all authentificated user to ask to create a project with POST
            if request.method == "POST":
                return bool(request.user and request.user.is_authenticated)

            # to all authentificated user to ask to create a project with POST
            else: # : request.method == "PUT" or request.method == "DELETE":
                print("test PUT OR DELETE")


                #reprendre ici, récup l'author_user_id du projet et le comparer à l'id de l'utilisateur connecté
                #si correspond, on autorise la modif et la suppression, sinon on aurotise pas.


                #here: pk and note project_pk : see the router design
                id_of_project_in_url = view.kwargs['pk']
                print("id_of_project_in_url", id_of_project_in_url)  # 19
                project_object = get_object_or_404(Project, pk=id_of_project_in_url)
                print("project_object", project_object)
                print("project_object.author_user_id", project_object.author_user_id)
                #REPRENDRE ICI : pour l'instant ca marche mais lorsque j'active les lignes ci dessous ca ne marche plus, juste une question d'objets et id
                #project_author = get_object_or_404(User, pk=project_object.author_user_id)
                #print("project_author", project_author)
                #print("request.user.id", request.user)


                #desactivation pour tests
                #return bool(request.user and request.user.is_authenticated and project_author == request.user)
                return bool(request.user and request.user.is_authenticated )



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
