from rest_framework import serializers
from recipes.models import Recipe

class TrendingRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['RecipeID', 'Title', 'Description', 'Owner', 'Ingredients', 'Difficulty', 'Category', 'rating', 'CookingTime', 'PrepTime']
    