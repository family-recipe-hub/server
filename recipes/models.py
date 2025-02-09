from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.
INGREDIENT_CATEGORY = [
    ('PRODUCE','Produce'),
    ('MEAT','Meat'),
    ('DAIRY','Diary'),
    ('GRAINS','Grains'),
    ('SPICES','Spices'),
    ('CONDIMENTS','Condiments'),
    ('BAKING','Baking'),
    ('BEVERAGES','Beverages')
]



DIFFICULTY_TYPE = [
    ('EASY','Easy'),
    ('MEDIUM','Medium'),
    ('HARD','Hard')
]



DIETARY_TYPE = [
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


class Ingredient(models.Model):
    Name = models.CharField(primary_key=True, max_length=100,null=False)
    Description = models.CharField(max_length=255)
    NutritionalInfo = models.JSONField()
    Category = models.CharField(max_length=100, choices=INGREDIENT_CATEGORY, default='PRODUCE')

    def __str__(self):
        return self.Name


class Recipe(models.Model):
    RecipeID = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    Title = models.CharField(max_length=50,null=False)
    Description = models.TextField(null=False)
    Ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    PrepSteps = ArrayField(models.JSONField(), blank=True)
    Difficulty = models.CharField(max_length=100, choices=DIFFICULTY_TYPE,null=False)
    Gallery = ArrayField(models.TextField(), blank=True)
    Category = models.CharField(max_length=50)
    VideoURL = models.CharField(max_length=200,null=True)
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )
    Language = ArrayField(models.CharField(max_length=100), blank=True)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, null = False)
    CookingTime = models.CharField(max_length=50)
    PrepTime = models.CharField(max_length=50)
    DietaryInfo = ArrayField(models.CharField(max_length=100, choices=DIETARY_TYPE, default='VEGAN'), blank=True)
    SeasonalTags = ArrayField(models.CharField(max_length=100), blank=True)
    Keywords = ArrayField(models.CharField(max_length=100), blank=True)
    PopularityScore = models.FloatField()

    def __str__(self):
        return self.Title



class RecipeVersions(models.Model):
    VersionID = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    RecipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False) 
    VersionNumber = models.IntegerField(null=False)
    Author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    Edits = models.TextField()


class Comments(models.Model):
    CommentID = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False)
    RecipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    Content = models.TextField(null=False)
    CreatedAt = models.DateTimeField(auto_now=True)


class RecipeIngredients(models.Model):
    RecipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False)
    IngredientName = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=False)
    Quantity = models.CharField(max_length=100)

class RecipeNutrition(models.Model):
    RecipeID = models.ForeignKey(Recipe, on_delete = models.CASCADE, null=False)
    ServingSize = models.CharField(max_length=100,null=False)
    Calories = models.IntegerField()
    Protein = models.FloatField()
    Carbohydrates = models.FloatField()
    Fat = models.FloatField()
    Fiber = models.FloatField()
    Vitamins = models.JSONField()
    Allergens = ArrayField(models.CharField(max_length=100))