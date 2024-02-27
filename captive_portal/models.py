from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model

class User(AbstractUser):
    """
    Represents a user in the system.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    class Meta:
        # Ensure that the custom User model is used
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return self.username
    
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')


class UserProfile(models.Model):
    """
    Represents a user profile in the system.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    network_id = models.CharField(max_length=100)
    network_name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the user profile.
        """
        return self.user.username
