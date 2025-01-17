from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import (
   AbstractBaseUser,
   BaseUserManager,
   PermissionsMixin
)

from phonenumber_field.modelfields import PhoneNumberField


class BaseUserModel(models.Model):
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
      abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set!')
        
        if not password:
            raise ValueError('The Password must be set!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self.db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    

class PromoCode(models.Model):
    code = models.CharField(unique=True, max_length=15)
    discount = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.code}"


class User(AbstractBaseUser, PermissionsMixin, BaseUserModel):
   username = None
   email = models.EmailField(unique=True)
   name = models.CharField(max_length=255)
   phone_number = PhoneNumberField(unique=True)

   address = models.TextField(max_length=500)

   promocode = models.CharField(max_length=255, null=True, blank=True)

   is_active = models.BooleanField(default=True)
   is_staff = models.BooleanField(default=False)

   objects = UserManager()

   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = ['name']

   class Meta:
      verbose_name = "User"
      verbose_name_plural = "Users"


   def __str__(self):
      return f"{self.name}: {self.email}"

   def save(self, *args, **kwargs):
      super().save(*args, **kwargs) 

   def has_perm(self, perm, obj=None):
      """Check if the user has a specific permission."""
      return True

   def has_module_perms(self, app_label):
      """Check if the user has permissions to access the specified app."""
      return True