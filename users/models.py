# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class User(AbstractUser):
    referral_code = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Specify custom related_name for one of the user_permissions fields
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
        help_text='Specific permissions for this user.'
    )

    # Specify a custom related_name for one of the groups fields
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
