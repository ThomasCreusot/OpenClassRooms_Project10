from rest_framework.serializers import ModelSerializer
 
from IssueTracking_app.models import Project, Issue, Comment, Contributor
#from authentication_app.models import User
 
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


class ContributorSerializer(ModelSerializer):
    """Serializes Contributors (users) objects"""

    class Meta:
        model = Contributor
        fields = ['id', 'user_id','project_id']

