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


def give_permission_to_contributors_of_a_project(view, request, view_kwarg_project):
    """Returns True if the authentified User is a collaborator of the given project"""
    #view_kwarg_project : pk or project_pk, see router design

    id_of_project_in_url = view.kwargs[view_kwarg_project]
    urlProject_and_RequestUser_contributor = Contributor.objects.filter(
        Q(project_id=id_of_project_in_url) & Q(user_id=request.user)
        ) 

    return bool(request.user and request.user.is_authenticated and urlProject_and_RequestUser_contributor)


def give_permission_to_author_of_a_project(view, request, view_kwarg_project):
    """Returns True if the authentified User is the author of the given project"""
    #view_kwarg_project : pk or project_pk, see router design

    id_of_project_in_url = view.kwargs[view_kwarg_project]
    project_object = get_object_or_404(Project, pk=id_of_project_in_url)

    return bool(request.user and request.user.is_authenticated and project_object.author_user_id == request.user)


def give_permission_to_author_of_an_issue(view, request, view_kwarg_issue):
    """Returns True if the authentified User is the author of the given project"""

    id_of_issue_in_url = view.kwargs[view_kwarg_issue]
    issue_object = get_object_or_404(Issue, pk=id_of_issue_in_url)

    return bool(request.user and request.user.is_authenticated and issue_object.author_user_id == request.user)




def give_permission_to_author_of_a_comment(view, request, view_kwarg_comment):
    """Returns True if the authentified User is the author of the given project"""

    id_of_comment_in_url = view.kwargs[view_kwarg_comment]
    comment_object = get_object_or_404(Comment, pk=id_of_comment_in_url)

    return bool(request.user and request.user.is_authenticated and comment_object.author_user_id == request.user)



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


    -ask to view a given Project   : contributors of a project AND project_author can ask to view details of the projects ; GET in has_object_permission
    -ask to create a given Project : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/projects/22
    -ask to update a given Project : project author only ; PUT in has_object_permission
    -ask to delete a given Project : project author only ; DELETE in has_object_permission
    """

    message = 'write an adequate message here : permissions.py ; ProjectsPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "POST":
            return bool(request.user and request.user.is_authenticated)
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_a_project(view, request, view_kwarg_project='pk')


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            contributor = give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='pk')
            author = give_permission_to_author_of_a_project(view, request, view_kwarg_project='pk')
            permission = contributor or author
            print(contributor)
            print(author)
            print(permission)
            return permission

            # only contributors, old version
            # return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='pk')
        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_a_project(view, request, view_kwarg_project='pk')










class IssuesPermission(BasePermission):
    """Gives permission :
    -ask to view all Issues of a project          : project contributors only ; GET in has_permission
    -ask to create all Issues of a project        : project contributors only ; POST in has_permission

    -ask to update all all Issues of a project    : PUT on http://127.0.0.1:8000/api/projects/23/issues : does not exist ; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
        --> Issue author only
    -ask to delete all all Issues of a project    : DELETE on http://127.0.0.1:8000/api/projects/23/issues : does not exist; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
        --> Issue author only

    -ask to view a given Issue of a given Project   : project contributors only ; GET in has_permission
    -ask to create a given Issue of a given Project : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/projects/22
    -ask to update a given Issue of a given Project : Issue author only ; PUT in has_object_permission
    -ask to delete a given Issue of a given Project : Issue author only ; DELETE in has_object_permission
    """

    message = 'write an adequate message here : permissions.py ; IssuesPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_an_issue(view, request, view_kwarg_issue='pk')


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_an_issue(view, request, view_kwarg_issue='pk')



class CommentPermission(BasePermission):
    """Gives permission :
    -ask to view all Comments of an Issue of a project          : project contributors only ; GET in has_permission
    -ask to create all Comments of an Issue of a project        : project contributors only ; POST in has_permission

    -ask to update all Comments of an Issue of a project    : PUT on http://127.0.0.1:8000/api/projects/23/issues : does not exist ; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
        --> Comment author only
    -ask to delete all Comments of an Issue of a project    : DELETE on http://127.0.0.1:8000/api/projects/23/issues : does not exist; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
        --> Comment author only

    -ask to view a given Comments of an Issue of a given Project   : project contributors only ; GET in has_permission
    -ask to create a given Comments of an Issue of a given Project : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/projects/22
    -ask to update a given Comments of an Issue of a given Project : Comment author only ; PUT in has_object_permission
    -ask to delete a given Comments of an Issue of a given Project : Comment author only ; DELETE in has_object_permission
    """

    message = 'write an adequate message here : permissions.py ; CommentPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_a_comment(view, request, view_kwarg_comment='pk')


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_a_comment(view, request, view_kwarg_comment='pk')







class ContributorsPermission(BasePermission):
    """
    /!\ role is to allow or not access to creation of contributors which are objects linking projects and users
     role is not to give or not access to contributors
    
    Gives permission :
    -ask to view all Contributors of a project          : Project contributors only ; GET in has_permission
    -ask to create all Contributors of a project        : Project author only ; POST in has_permission

    -ask to update all all Contributors of a project    : PUT on http://127.0.0.1:8000/api/projects/23/issues : does not exist ; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
        --> Project author only
    -ask to delete all all Contributors of a project    : DELETE on http://127.0.0.1:8000/api/projects/23/issues : does not exist; but same code as in has_object_permission, as :
        "The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed."
        (https://www.django-rest-framework.org/api-guide/permissions/)
        --> Project author only

    -ask to view a given Contributor of a given Project   : project contributors only ; GET in has_permission
    -ask to create a given Contributor of a given Project : "Method \"POST\" not allowed." on http://127.0.0.1:8000/api/projects/22
    -ask to update a given Contributor of a given Project : Project author only ; PUT in has_object_permission
    -ask to delete a given Contributor of a given Project : Project author only ; DELETE in has_object_permission
    """

    message = 'write an adequate message here : permissions.py ; ContributorsPermission'


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "POST":
            return give_permission_to_author_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_a_project(view, request, view_kwarg_project='project_pk')


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return give_permission_to_contributors_of_a_project(view, request, view_kwarg_project='project_pk')
        elif request.method == "POST":
            return False  # "Method \"POST\" not allowed."
        elif request.method == "PUT" or request.method == "DELETE":
            return give_permission_to_author_of_a_project(view, request, view_kwarg_project='project_pk')

