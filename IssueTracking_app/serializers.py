from rest_framework.serializers import ModelSerializer
 
from IssueTracking_app.models import Project, Issue, Comment, Contributor
from authentication_app.models import User
 
#versionBefore list/detail serializers
#class ProjectSerializer(ModelSerializer):
#    """Serializes Project objects"""
#
#    class Meta:
#        model = Project
#        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']


class ProjectListSerializer(ModelSerializer):
    """Serializes Project objects"""

    class Meta:
        model = Project
        #fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

# http://127.0.0.1:8000/api/projects/2/
# 'contributors' --> list of USERS id, not 'contributors as relation between project and User' : NICE !
class ProjectDetailSerializer(ModelSerializer):
    """Serializes Project objects"""

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']


class IssueSerializer(ModelSerializer):
    """Serializes Issue objects"""

    class Meta:
        model = Issue
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id', 'created_time']


class CommentSerializer(ModelSerializer):
    """Serializes Comment objects"""

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']




# Solution A for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorSerializer(ModelSerializer):
    """Serializes Contributors (as contributors) objects"""

    class Meta:
        model = Contributor
        fields = ['id', 'user_id','project_id', 'role']

# Solution B for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorUserSerializer(ModelSerializer):
    """Serializes Contributors (as users) objects"""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Solution C.1/2 for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorUserDetailSerializer(ModelSerializer):
    """Serializes users objects who will be displayed as part of contributors objects"""

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Solution C.2/2 for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorCompleteSerializer(ModelSerializer):
    """Serializes Contributors (as contributors) objects"""

    user_id = ContributorUserDetailSerializer(many=False)

    class Meta:
        model = Contributor
        fields = ['id', 'user_id','project_id', 'role']