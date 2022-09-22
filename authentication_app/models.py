from django.db import models

from django.contrib.auth.models import AbstractUser

#Cours OC : Même si modèle  User  par défaut tout à fait convenable, : conseille de toujours
# implémenter un modèle  User  personnalisé dans votre projet. Et ce, même s’il est identique au
# modèle par défaut ! […]
class User(AbstractUser):
    """Reprensents an User"""
    # user_id = models.fields.IntegerField   # already in the AbstractUser model
    # first_name = models.fields.CharField  # already in the AbstractUser model
    # last_name = models.fields.CharField  # already in the AbstractUser model
    # email = models.fields.EmailField   # already in the AbstractUser model
    # password = models.fields.CharField   # already in the AbstractUser model
    pass
