from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class UserProfile(models.Model):
    """
    Represents a user profile in the system.
    """

    username = models.CharField(max_length=100)
    email = models.EmailField()
    agreed_to_terms = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the user profile.
        """
        return self.username

class User(AbstractUser):
    """
    Represents a user in the system.
    """
    email = models.EmailField(unique=True)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    username= models.CharField(max_length=20, unique=True)

    class Meta:
        # Ensure that the custom User model is used
        swappable = 'AUTH_USER_MODEL'

    # Specify unique related_name arguments for groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
