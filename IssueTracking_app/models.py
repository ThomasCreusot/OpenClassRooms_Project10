from django.db import models
from django.conf import settings

# https://docs.djangoproject.com/en/4.1/ref/models/fields/ : 
# --Null is purely database-related, whereas blank is validation-related.
# Avoid using null on string-based fields ; One exception is when a CharField has both unique=True
# and blank=True set. In this situation, null=True is required to avoid unique constraint
# violations when saving multiple objects with blank values.
# --Choices: The first element in each tuple is the actual value to be set on the model, and the
# second element is the human-readable name

class Project(models.Model):
    """Represents a project/product/application under development or management : an entity which
    has several collaborators and which can contain several issues"""

    BACKEND = 'BE'
    FRONTEND = 'FE'
    IOS = 'IOS'
    ANDROID ='ANDROID'

    TYPE_CHOICES = (
        (BACKEND, 'back-end'),
        (FRONTEND, 'front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android'),
    )

    # project_id = models.fields.IntegerField  # by default in Django
    title = models.fields.CharField(max_length=255, blank=False)
    # description field: blank = False : conception document: "doit avoir..."
    description = models.fields.CharField(max_length=2000, blank=False)
    type = models.fields.CharField(max_length=255, choices=TYPE_CHOICES, blank=False)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='projectAuthor')
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor',
        related_name='contributions')


class Contributor(models.Model):
    """A through table wich reprensents the relation between User and Project classes"""

    # user_id = models.fields.IntegerField  # version in softDesk conception document
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # project_id = models.fields.IntegerField  # version in softDesk conception document
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.fields.CharField(max_length=255, blank=False)

    class Meta:
        unique_together = ('user_id', 'project_id')


class Issue(models.Model):
    """Represents an isssue happening during a Project"""

    HIGH_PRIORITY = 'HP'
    INTERMEDIATE_PRIORITY = 'IP'
    LOW_PRIORITY = 'LP'

    BUG = 'BU'
    IMPROVEMENT =  'IMP'
    TASK = 'TA'

    TO_BE_DONE = 'TBD'
    ON_GOING =  'OG'
    DONE = 'DO'

    PRIORITY_CHOICES = (
        (HIGH_PRIORITY, 'Faible'),
        (INTERMEDIATE_PRIORITY, 'Moyenne'),
        (LOW_PRIORITY, 'Élevée'),
    )

    TAG_CHOICES = (
        (BUG, 'Bug'),
        (IMPROVEMENT, 'Amélioration'),
        (TASK, 'Tache'),
    )

    STATUS_CHOICES = (
        (TO_BE_DONE, 'A faire'),
        (ON_GOING, 'En cours'),
        (DONE, 'Terminé'),
    )

    title = models.fields.CharField(max_length=255, blank=False)
    # desc field: blank = False : conception document: "doit avoir..."
    desc = models.fields.CharField(max_length=2000, blank=False) 
    tag = models.fields.CharField(max_length=255, choices=TAG_CHOICES, blank=False)
    priority = models.fields.CharField(max_length=255, choices=PRIORITY_CHOICES, blank=False)
    #project_id = models.fields.IntegerField  # version in softDesk conception document
    project_id = models.ForeignKey(Project, blank=False, on_delete=models.CASCADE,
        related_name='issueProject')
    status = models.fields.CharField(max_length=255, choices=STATUS_CHOICES, blank=False)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='issueAuthor')
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False,
        on_delete=models.CASCADE, related_name='issueAssignee')
    created_time = models.fields.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Represent a comment of a given issue"""

    #comment_id = models.fields.IntegerField   # by default in Django
    # description field:  blank = False : document de conception : "doit avoir..."
    description = models.fields.CharField(max_length=255, blank=False)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='commentAuthor')
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='commentIssue')
    created_time = models.fields.DateTimeField(auto_now_add=True)
