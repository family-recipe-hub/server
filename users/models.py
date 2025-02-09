from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
import uuid


USER_TYPE_CHOICES = [
  ('COOKER', 'Cooker'),
  ('PROFESSIONAL_CHEF', 'Professional Chef'),
  ('NUTRITIONIST', 'Nutritionist'),
  ('NORMAL_USER', 'Normal user'),
]

DIETARY_TYPE_CHOICES = [
  ('VEGAN', 'Vegan'),
  ('VEGETARIAN', 'Vegetarian'),
  ('GLUTEN_FREE', 'Gluten free'),
  ('DAIRY_FREE', 'Dairy free'),
  ('NUT_FREE', 'Nut free'),
  ('LOW_CARB', 'Low carb'),
  ('LOW_FAT', 'Low fat'),
  ('HALAL', 'Halal'),
  ('KOSHER', 'Kosher'),
  ('PALEO', 'Paleo'),
]

class CustomUserManager(BaseUserManager):
  """
  The create_user method is used to create a regular user with basic authentication functionality.
  """
  def create_user(self, email, username, password, **extra_fields):
    if not email:
      raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    user = self.model(username=username , email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)

    return user

  """
  The create_superuser method is used to create a superuser with basic authentication functionality.
  """
  def create_superuser(self, email, username, password, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    return self.create_user(email, username, password, **extra_fields)
  
class User(AbstractBaseUser, PermissionsMixin):
  """
  The User model is used to store user information.
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.EmailField(max_length=100, unique=True)
  username = models.CharField(max_length=100, unique=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  """Replaces default user manager with a custom implementation"""
  objects = CustomUserManager()


  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username']

  def __str__(self):
    return self.email
  
  def has_perm(self, perm, obj=None):
      """Check if user has a specific permission"""
      return self.is_superuser

  def has_module_perms(self, app_label):
      """Check if user has permissions for a specific app"""
      return self.is_superuser

  

class Profile(models.Model):
  """
  The Profile model is used to store user profile information.
  """
  user = models.OneToOneField(User, related_name= 'profile', on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=20, null=True, blank=True)
  profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
  user_type = models.CharField(max_length=100, choices=USER_TYPE_CHOICES, default='NORMAL_USER')
  languages = ArrayField(models.CharField(max_length=100), default=list, blank=True, null=True)
  country = models.CharField(max_length=100)
  dietary_restrictions = models.CharField(max_length=100, choices=DIETARY_TYPE_CHOICES, default='VEGAN')
  cooking_goals = ArrayField(models.CharField(max_length=100), default=list, blank=True, null=True)
  favorite_tools = ArrayField(models.CharField(max_length=100), default=list, blank=True, null=True)
  biography = models.TextField(blank=True, null=True)
  social_links = models.JSONField(blank=True, null=True)
  preferences = models.JSONField(blank=True, null=True)
  notification_settings = models.JSONField(blank=True, null=True)
  following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"
