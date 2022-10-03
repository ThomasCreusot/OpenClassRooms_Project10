from django.contrib.auth.models import AbstractUser

# OC classes: even if the User model by default is appropriate, we advice to # always implement a
# personalizerd User model (even if identical to defaul model)
class User(AbstractUser):
    """Reprensents an User"""
    # user_id = models.fields.IntegerField   # already in the AbstractUser model
    # first_name = models.fields.CharField  # already in the AbstractUser model
    # last_name = models.fields.CharField  # already in the AbstractUser model
    # email = models.fields.EmailField   # already in the AbstractUser model
    # password = models.fields.CharField   # already in the AbstractUser model
    pass
