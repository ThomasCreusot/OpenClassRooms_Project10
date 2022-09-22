from rest_framework.serializers import ModelSerializer
 
from IssueTracking_app.models import Project

 
class ProjectSerializer(ModelSerializer):
    """Serializes Project objects"""

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user_id', 'contributors']

