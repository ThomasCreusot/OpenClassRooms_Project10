# OpenClassRooms_Project10
Create a secure RESTful API using Django REST


# Project presentation
The present project is the tenth one of the training course *Python Application Developer*, offered by OpenClassRooms and aims to *Create a secure RESTful API using Django REST*.

The main goal is to develop an **issue tracking system** wich allows users to **create and manage technical issues of projects**. 

This API must:
- Be useful for websites and applications (Android and iOS)
- Allow users to: create projects, add contributors (users) to projects, create issues related to projects and write comments related to issues.

Specifications:
- Signup and login: use JWT authentification (tokens)
- Project is an entity which got collaborators (users), and each project can contain issues. A project is caracterised by a title, a description, a type (back-end, front-end, iOS or Android) and an author_user_id
- A project is accessible only to its author and contributors
- An user can CRUD an issue only if he/she is a contributor of the project.
- An issue is caracterised by a title, a description, an assignee, a priority, a tag, a status, a project_id and a created_time
- Contributors of a project can comment an issue. A comment is caracterised by a description, an author_user_id, an issue_id and a comment_id.
- **A project/issue/comment can be updated or deleted only by its author.**

- For more details, please refer to the [endpoints documentation](https://documenter.getpostman.com/view/20371598/2s83tCLDEC).


# Project execution
To correctly execute the program, you need to activate the associated virtual environment which has been recorded in the ‘requirements.txt’ file.

## To create and activate the virtual environment 
Please follow theses instructions:

1. Open your Shell 
-Windows: 
>'windows + R' 
>'cmd'  
-Mac: 
>'Applications > Utilitaires > Terminal.app'

2. Find the folder which contains the program (with *cd* command)

3. Create a virtual environment: write the following command in the console
>'python -m venv env'

4. Activate this virtual environment: 
-Linux or Mac: write the following command in the console
>'source env/bin/activate'
-Windows: write the following command in the console 
>'env\Scripts\activate'

5. Install the python packages recorded in the *requirements.txt* file: write in the console the following command
>'pip install -r requirements.txt'

## To launch the server
Please follow this instruction
6. Execute the code: write the following command in the console (Python must be installed on your computer and virtual environment must be activated)
>'python manage.py runserver'

## To access to the API
7. Open POSTMAN (for example) and create an account by making a POST request on http://127.0.0.1:8000/api/signup/
Please, write the following fields in the request body: username, password, first_name, last_name, email with the value of your choice.

8. Once your account is created, you can make a POST request on http://127.0.0.1:8000/api/token/ to get an access Token.
Please, write the following fields in the request body: username, password with the value you chosen at the previous step.

9. Then, write the following field in the request header: Authorization, with the value "Bearer TOKEN" (replace "TOKEN" by the value of your current access token, that you get at the previous step).

10. Please enjoy the API ; you can, for example make a GET request on http://127.0.0.1:8000/api/projects/ to see all projects you are involved in.


# Example of request, response and corresponding code
The example chosen is a user who make a GET request on http://127.0.0.1:8000/api/projects/30/issues/ to get all issues of a project (project id = 30) in which he/she is involved as collaborator. 

## Example of request and response 

### Request
```
curl --location --request GET 'http://127.0.0.1:8000/api/projects/30/issues/' \
--header 'Authorization: Bearer TOKEN' \
```

### API response
All issues related to the project 30
```json
[
    {
        "id": 49,
        "title": "first issue of project 30 updated",
        "desc": "IMProvement of LowPriority with status DOne updated",
        "tag": "IMP",
        "priority": "LP",
        "project_id": "Project object (30)",
        "status": "DO",
        "author_user_id": "user12",
        "assignee_user_id": "user12",
        "created_time": "2022-09-30T10:43:07.106258Z"
    },
    {
        "id": 50,
        "title": "Second issue of project 30",
        "desc": "BUg of High Priority with status To Be Done",
        "tag": "BU",
        "priority": "HP",
        "project_id": "Project object (30)",
        "status": "TBD",
        "author_user_id": "user12",
        "assignee_user_id": "user12",
        "created_time": "2022-10-03T08:50:17.887944Z"
    }
]
```

## Corresponding code

### urls.py
```python
projects_issues_router = routers.NestedSimpleRouter(router, 'projects', lookup='project')
projects_issues_router.register('issues', IssueViewset, basename='project-issues')
```

### views.py
```python
class IssueViewset(ModelViewSet):
    """API endpoint that allows Issues to be CRUD."""

    serializer_class = IssueSerializer 

    permission_classes = [IssuesPermission]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs['project_pk'])
```

### serializers.py
```python
class IssueSerializer(ModelSerializer):
    """Serializes Issue objects"""

    author_user_id = serializers.CharField(default=0)
    assignee_user_id = serializers.CharField(default=0)
    project_id = serializers.CharField(default=0)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id', 'status', 
                  'author_user_id', 'assignee_user_id', 'created_time']

    def save(self):
        id_of_project_in_url = self.context['view'].kwargs['project_pk']
        project_object = get_object_or_404(Project, pk=id_of_project_in_url)

        super().save(author_user_id = self.context['request'].user, 
                     assignee_user_id = self.context['request'].user,
                     project_id = project_object
                     )
```

### permissions.py
```python
def give_permission_to_contributors_of_a_project(view, request, view_kwarg_project):
    """Returns True if the authenticated User is a collaborator of the given project"""
    #view_kwarg_project : pk or project_pk, see router design

    id_of_project_in_url = view.kwargs[view_kwarg_project]
    urlProject_and_RequestUser_contributor = Contributor.objects.filter(
        Q(project_id=id_of_project_in_url) & Q(user_id=request.user)
        ) 

    return bool(request.user and request.user.is_authenticated and urlProject_and_RequestUser_contributor)


def give_permission_to_author_of_an_issue(view, request, view_kwarg_issue):
    """Returns True if the authenticated User is the author of the given project"""

    id_of_issue_in_url = view.kwargs[view_kwarg_issue]
    issue_object = get_object_or_404(Issue, pk=id_of_issue_in_url)

    return bool(request.user and request.user.is_authenticated and issue_object.author_user_id == request.user)


class IssuesPermission(BasePermission):
    """Gives permission:
    -ask to view all Issues of a project           : project contributors only; GET in has_permission
    -ask to create all Issues of a project         : project contributors only; POST in has_permission
    [...]
    -ask to view a given Issue of a given Project  : project contributors only, GET in has_object_permission
    -ask to create a given Issue of a given Project: "Method \"POST\" not allowed."
    -ask to update a given Issue of a given Project: Issue author only ; PUT in has_object_permission
    -ask to delete a given Issue of a given Project: Issue author only ; DELETE in has_object_permission
    """

    message = 'You are not allowed to do this action, see permissions.py / IssuesPermission'

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
```
