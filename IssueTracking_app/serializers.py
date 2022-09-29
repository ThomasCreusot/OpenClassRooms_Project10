
from email.policy import default
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from IssueTracking_app.models import Project, Issue, Comment, Contributor
from authentication_app.models import User

from django.shortcuts import get_object_or_404

#versionBefore list/detail serializers
#class ProjectSerializer(ModelSerializer):
#    """Serializes Project objects"""
#
#    class Meta:
#        model = Project
#        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']


class ProjectListSerializer(ModelSerializer):
    """Serializes Project objects"""

    #https://www.django-rest-framework.org/api-guide/fields/#core-arguments
    #Initial : A value that should be used for pre-populating the value of HTML form fields. You may pass a callable to it, just as you may do with any regular Django Field:


    # ESSAIS pour valeur par défaut sur Author user id ; résolu en surchargeant la méthode save() 
    #author_user_id = serializers.CharField(initial=serializers.CurrentUserDefault())
    #author_user_id = serializers.CharField(initial=serializers.CurrentUserDefault()) # utiliser la classe d'authentification : permet de définir l’utilisateur à l’origine de la requête. C’est elle qui attache le user  à la requête avec l’attribut request.user  si l'utilisateur a prouvé son authentification (page 47/57 cours 010.1)
    #author_user_id = serializers.CharField(initial=serializers.CurrentUserDefault())
    author_user_id = serializers.CharField(initial="Current user by default by overwriting  save() method ; replace 'Charfield' by 'HiddenField' and 'initial' by 'default' in the present line to hide the field")

    class Meta:
        model = Project
        #fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']
        fields = ['id', 'title', 'description', 'type', 'author_user_id']

    def save(self):
        #self.author_user_id = self.context['request'].user
        #print("author_user_id saved as self.context['request'].user", self.context['request'].user)
        #Overwriting save method with defining the author_user_id
        super().save(author_user_id = self.context['request'].user)


# http://127.0.0.1:8000/api/projects/2/
# 'contributors' --> list of USERS id, not 'contributors as relation between project and User' : NICE !
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
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id', 'created_time']

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


    def validation_to_avoid_duplicate_project_user_couple(self, project, user):
        """Avoids creation of duplicates Contributor objects"""

        #instead of validate() which is executeed before save()

        print(project)
        print(user)

        # Recherche d'objets Contributor qui ont le project_id que l'on est en train de renseigner pour la création d'un nouvel objet contributor
        if Contributor.objects.filter(project_id=project, user_id=user).exists():
            raise serializers.ValidationError('A contributor relation between this project and this user already exists')


    def save(self):
        #j'écris ma propre validation, car si j'utilise validate(); elle est appelée avant ma méthode save, donc le projet a comme valeur sa valeur par défaut 

        id_of_project_in_url = self.context['view'].kwargs['project_pk']
        #print("save() : id_of_project_in_url", id_of_project_in_url)
        project_object = get_object_or_404(Project, pk=id_of_project_in_url)

        self.validation_to_avoid_duplicate_project_user_couple(project_object, self.validated_data['user_id'])

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