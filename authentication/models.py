from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_new_intra_user(self, user_intra):
        try:
            user = self.get(username=user_intra['login'])
        except self.model.DoesNotExist:
            user = self.create(
                username=user_intra['login'],
                email=user_intra['email'],
                profile_picture_url=user_intra['image']['versions']['medium']
            )
        return user


class CustomUser(AbstractUser):
    profile_picture_url = models.URLField(max_length=200, blank=True, null=True)

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name=('groups'),
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        blank=True,
        help_text=('Specific permissions for this user.'),
        verbose_name=('user permissions'),
    )

    def __str__(self):
        return self.username
