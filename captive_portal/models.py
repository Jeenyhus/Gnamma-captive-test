from django.db import models
from django.contrib.auth.models import AbstractUser

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
