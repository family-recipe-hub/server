from django.db import models
from recipes.models import Recipe

# Create your models here.

class RecipeTrendalytics(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name="trends", primary_key=True)
    last_like_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.recipe.Title
    