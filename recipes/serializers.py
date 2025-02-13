from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeVersions, Comments,  RecipeNutrition


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('Name', 'Description', 'NutritionalInfo', 'Category')




class RecipeSerializer(serializers.ModelSerializer):
    Ingredients = IngredientSerializer(many=True)
    class Meta:
        model = Recipe
        exclude = ['RecipeID']





class RecipeVersionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeVersions
        fields = ('RecipeID', 'VersionNumber', 'Author', 'Edits')




class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('RecipeID', 'UserID', 'Content', 'CreatedAt')




class RecipeNutritionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecipeNutrition
        fields = ('__all__')
