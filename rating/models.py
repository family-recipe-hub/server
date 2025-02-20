from django.db import models
from django.contrib.auth import get_user_model
from recipes.models import Recipe
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
# Create your models here.

User = get_user_model()

def CustomValidator(value):
    if value * 2 != int(value * 2):
        raise ValidationError("the number must be whole or half number")



class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='ratings')
    stars = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5),CustomValidator])

    class Meta():
        unique_together = ('user','recipe')

