from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, role='tenant', **extra_fields):
        """
        Creates and saves a user with the given username, email, first name, and last name.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            role=role,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given details.
        """
        user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role='staff',
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_landlord(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a landlord user.
        """
        return self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role='landlord',
            **extra_fields
        )

    def create_tenant(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a tenant user.
        """
        return self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role='tenant',
            **extra_fields
        )




class UserAccount(AbstractUser, PermissionsMixin):
    class Role(models.TextChoices):
        STAFF = 'staff', 'staff'
        LANDLORD = 'landlord', 'landlord'
        TENANT = 'tenant', 'tenant'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TENANT)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'  # <- Make email the username field for authentication
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # Fields required when creating superuser

    def __str__(self):
        return self.email

