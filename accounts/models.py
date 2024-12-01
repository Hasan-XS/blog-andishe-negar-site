from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import random


class CustomUser(AbstractUser):
    """
    CustomUser extends the AbstractUser model to include additional fields for email verification.

    Fields:
        is_email_verified (BooleanField): Indicates whether the user's email has been verified. Default is False.
        email_verification_code (CharField): Stores the email verification code. This field is optional and can be blank or null.

    Relationships:
        groups (ManyToManyField): Establishes a many-to-many relationship with the Group model, allowing the user to belong to multiple groups.
        user_permissions (ManyToManyField): Establishes a many-to-many relationship with the Permission model, allowing the user to have specific permissions.

    Methods:
        generate_verification_code: Generates a random 6-digit verification code as a string to be sent for email verification.
    """

    is_email_verified = models.BooleanField(default=False)
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )

    def generate_verification_code(self):
        """
        Generates a 6-digit random verification code.

        Returns:
            str: A 6-digit random verification code.
        """
        return str(random.randint(100000, 999999))
