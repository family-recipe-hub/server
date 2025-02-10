from rest_framework import serializers
from recipes.models import Recipe

class RecipeSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients']
