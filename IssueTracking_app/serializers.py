from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from IssueTracking_app.models import Project, Issue, Comment, Contributor

# versionBefore list/detail serializers
#class ProjectSerializer(ModelSerializer):
#    """Serializes Project objects"""
#
#    class Meta:
#        model = Project
#        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']

class ProjectListSerializer(ModelSerializer):
    """Serializes Project objects"""

    #Current user by default by overwriting  save() method ; replace 'Charfield' by 'HiddenField'
    # and 'initial' by 'default' in the present line to hide the field
    author_user_id = serializers.CharField(initial="initial value in ProjectListSerializer")

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def save(self):
        super().save(author_user_id = self.context['request'].user)


class ProjectDetailSerializer(ModelSerializer):
    """Serializes Project objects"""

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']


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


class CommentSerializer(ModelSerializer):
    """Serializes Comment objects"""

    author_user_id  = serializers.CharField(default=0)
    issue_id = serializers.CharField(default=0)

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']


    def save(self):
        id_of_issue_in_url = self.context['view'].kwargs['issue_pk']
        issue_object = get_object_or_404(Issue, pk=id_of_issue_in_url)

        super().save(author_user_id = self.context['request'].user, 
                     issue_id = issue_object
                     )


# Solution A for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorSerializer(ModelSerializer):
    "Serializes Contributors (as contributors) objects"

    project_id = serializers.CharField(default=0)

    class Meta:
        model = Contributor
        fields = ['id', 'user_id','project_id', 'role']


    # Our own validation method, instead of validate() which is executeed before save()
    def validation_to_avoid_duplicate_project_user_couple(self, project, user):
        """Avoids creation of duplicates Contributor objects"""

        # Look at Contributor objects which has the same project_id as the one we are filling in
        # for creation of a new Contributor object
        if Contributor.objects.filter(project_id=project, user_id=user).exists():
            raise serializers.ValidationError('You are already a contributor of this project')


    def save(self):
        id_of_project_in_url = self.context['view'].kwargs['project_pk']
        project_object = get_object_or_404(Project, pk=id_of_project_in_url)
        self.validation_to_avoid_duplicate_project_user_couple(project_object,
            self.validated_data['user_id'])

        super().save(project_id = project_object)


"""
# Solution B for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorUserSerializer(ModelSerializer):
    "Serializes Contributors (as users) objects"

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Solution C.1/2 for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorUserDetailSerializer(ModelSerializer):
    "Serializes users objects who will be displayed as part of contributors objects"

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# Solution C.2/2 for http://127.0.0.1:8000/api/projects/2/contributors/
class ContributorCompleteSerializer(ModelSerializer):
    "Serializes Contributors (as contributors) objects"

    user_id = ContributorUserDetailSerializer(many=False)

    class Meta:
        model = Contributor
        fields = ['id', 'user_id','project_id', 'role']
"""