from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FamilyGroup(models.Model):
    admin = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_family_groups")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200,null=True,blank=True)
    code = models.CharField(max_length=50,unique=True)
    
class Recipe(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_recipes')
    pass

class Collection(models.Model):

    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_collections')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200,null=True,blank=True)
    is_public = models.BooleanField(default=True)
    recipes = models.ManyToManyField(Recipe,related_name='collection_recipes')
    

# stores the family group members
class Membership(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,related_name='my_memberships')
    family = models.ForeignKey(FamilyGroup,on_delete=models.CASCADE,related_name="group_members")
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user','family')

class GroupCollection(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_members')
    family_group = models.ForeignKey(FamilyGroup,on_delete=models.CASCADE,related_name='group_collections')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200,null=True,blank=True)
    recipes = models.ManyToManyField(Recipe,related_name='group_collection_recipes')
    