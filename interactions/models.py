from django.db import models
from users.models import User
from recipes.models import Recipe
from recipes.models import Ingredient
import uuid

# Create your models here.

class RecipeComments(models.Model):
    CommentID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Recipe = models.ForeignKey(Recipe, null=False,  on_delete=models.CASCADE)
    User = models.ForeignKey(User, null=False,  on_delete=models.CASCADE)
    Content = models.TextField(null=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.User} on Recipe {self.Recipe}"

class RecipeUpdateRequests(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]
    RequestID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Recipe = models.ForeignKey(Recipe, null=False, on_delete=models.CASCADE)
    ProposalEdits = models.TextField(null=False)
    UserRequested = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')


    def __str__(self):
        return f"Update Request for Recipe {self.Recipe} by {self.UserRequested}"


class Playlist(models.Model):
    PlaylistID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, null=False)


class Favorite(models.Model):
    FavoriteID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Recipe = models.ForeignKey(Recipe, null=False, on_delete=models.CASCADE)
    Ingredient = models.ForeignKey(Ingredient, null=True, on_delete=models.SET_NULL)
    SavedAt = models.DateTimeField(auto_now_add=True, null=False)
    Playlist = models.ForeignKey(Playlist, null=False, on_delete=models.CASCADE)
    
class Notification(models.Model):
    NotificationID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    User = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    Read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.User}"


