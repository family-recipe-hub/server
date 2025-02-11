from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeVersions, Comments, RecipeIngredients, RecipeNutrition


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('Name', 'Description', 'NutritionalInfo', 'Category')




class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    owner = serializers.IntegerField(source="Owner.id", read_only=True)  

    class Meta:
        model = Recipe
        fields = (  'Title', 'Description', 'Ingredients', 'PrepSteps',
                    'Difficulty', 'Gallery', 'Category', 'VideoURL',
                    'rating', 'Language', 'Owner', 'CookingTime',
                    'PrepTime', 'DietaryInfo', 'SeasonalTags', 'PopularityScore')

    def get_Ingredients(self, obj):
        return list(obj.Ingredients.values_list("Name", flat=True))




class RecipeVersionsSerializer(serializers.ModelSerializer):
    RecipeId = serializers.IntegerField(source="Recipe.RecipeID", read_only=True)
    Author = serializers.IntegerField(source="Author.id", read_only=True)

    class Meta:
        model = RecipeVersions
        fields = ('RecipeID', 'VersionNumber', 'Author', 'Edits')




class CommentsSerializer(serializers.ModelSerializer):
    RecipeId = serializers.IntegerField(source="Recipe.RecipeID", read_only=True)
    UserID = serializers.IntegerField(source="UserID.id", read_only=True)

    class Meta:
        model = Comments
        fields = ('RecipeID', 'UserID', 'Content', 'CreatedAt')




class RecipeIngredientsSerializer(serializers.ModelSerializer):
    RecipeId = serializers.IntegerField(source="Recipe.RecipeID", read_only=True)
    IngredientName = serializers.CharField(source="IngredientName.Name")
    class Meta:
        model = RecipeIngredients
        fields = ("__all__")



class RecipeNutritionSerializer(serializers.ModelSerializer):
    RecipeId = serializers.IntegerField(source="Recipe.RecipeID", read_only=True)

    class Meta:
        model = Ingredient
        fields = ("__all__")
