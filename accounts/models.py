from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomerCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    discount_percentage = models.FloatField(default=0)
    minimum_order = models.IntegerField()
    maximum_order = models.IntegerField()


    class Meta:
        verbose_name_plural = 'customer categories'

    def __str__(self):
        return self.name

class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, first_name, last_name, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, password=password,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        customer_category = CustomerCategory.objects.filter(name='Bronze').first()
        print(user)
        print("Category", customer_category)
        user.customer_category = customer_category
        user.save()
        print(user)
        return user

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class Account(AbstractUser):
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    department = models.ForeignKey('Department', null=True, on_delete=models.CASCADE, blank=True)
    customer_category = models.ForeignKey('CustomerCategory', null=True, on_delete=models.SET_NULL, blank=True)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'
    objects = AccountManager()




class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name



