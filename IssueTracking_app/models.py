from django.db import models
#from django.contrib.auth.models import AbstractUser
from django.conf import settings

#TO DO LIST
#table through Contribors; champ permission : choicefield : retrouver les intitulés des choix
#Consignes OC : le lien entre la table users et la table projects est redondant : implementez le uniquement si cela vous facilite la tache


# https://docs.djangoproject.com/en/4.1/ref/models/fields/ : 
# null is purely database-related, whereas blank is validation-related.
# Avoid using null on string-based fields ; One exception is when a CharField has both unique=True
# and blank=True set. In this situation, null=True is required to avoid unique constraint
# violations when saving multiple objects with blank values.

# https://docs.djangoproject.com/en/4.1/ref/models/fields/ : 
# Choices: The first element in each tuple is the actual value to be set on the model, and the
# second element is the human-readable name


#MODELE USER DEPLACE dans authentication app



# Elle entretient une relation plusieurs-à-plusieurs avec la table des utilisateurs, via une table
# de jonction appelée Contributors.
# Par souci de simplicité, nous avons également ajouté une relation un-à-plusieurs avec la table
# Users, de sorte que nous pouvons enregistrer l'auteur/le responsable/le créateur du projet.
# Vous pouvez également gérer ce cas à l'aide du champ d'autorisation de la classe Contributor
class Project(models.Model):
    """Represents a project/product/application under development or management :
    an entity which has several collaborators and which can contain several issues"""

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
    description = models.fields.CharField(max_length=2000, blank=False)  # blank = False : document de conception : "doit avoir..."

    type = models.fields.CharField(max_length=255, choices=TYPE_CHOICES, blank=False)

    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projectAuthor')

    #added
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='contributions')


#THROUGH TABLE
class Contributor(models.Model):
    """A through table wich reprensents the relation between User and Project classes"""

    #PERMISSION1 = 'PERMISSION1'
    #PERMISSION2 = 'PERMISSION2'

    #PERMISSION_CHOICES = (
    #    (PERMISSION1, 'aretrouver'),
    #    (PERMISSION2, 'aretrouver'),
    #)

    # user_id = models.fields.IntegerField  # version in softDesk conception document
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # project_id = models.fields.IntegerField  # version in softDesk conception document
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    # permission = models.fields.ChoiceField  # ChoiceField ? I choose a Charfield with a choices property
    #CorentinB 21092022:Tu n'es pas obligé d'utiliser ce champ permission. Je crois que plusieurs étudiants l'ont ignoré parce qu'il y avait de meilleurs moyens de déterminer les permissions.
    #permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES, verbose_name='Permission')

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
    desc = models.fields.CharField(max_length=2000, blank=False)  # blank = False : document de conception : "doit avoir..."
    #tag = balise
    tag = models.fields.CharField(max_length=255, choices=TAG_CHOICES, blank=False)
    priority = models.fields.CharField(max_length=255, choices=PRIORITY_CHOICES, blank=False)

    #project_id = models.fields.IntegerField  # version in softDesk conception document
    project_id = models.ForeignKey(Project, blank=False, on_delete=models.CASCADE, related_name='issueProject')

    status = models.fields.CharField(max_length=255, choices=STATUS_CHOICES, blank=False)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='issueAuthor')

    # assignee_user_id : Utilisateur auquel le problème est affecté
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE, related_name='issueAssignee')

    created_time = models.fields.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Represent a comment of a given issue"""
    #comment_id = models.fields.IntegerField   # by default in Django
    description = models.fields.CharField(max_length=255, blank=False)  # blank = False : document de conception : "doit avoir..."
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commentAuthor')
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='commentIssue')
    created_time = models.fields.DateTimeField(auto_now_add=True)
