from rest_framework import serializers
from .models import Ingredient, Recipe, RecipeVersions, Comments, RecipeIngredients, RecipeNutrition


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('Name', 'Description', 'NutritionalInfo', 'Category')




class RecipeSerializer(serializers.ModelSerializer):
    Ingredients = serializers.SerializerMethodField()
    Owner = serializers.UUIDField(source="Owner.id", read_only=True)  

    class Meta:
        model = Recipe
        fields = (  'Title', 'Description', 'Ingredients', 'PrepSteps',
                    'Difficulty', 'Gallery', 'Category', 'VideoURL',
                    'rating', 'Language', 'Owner', 'CookingTime',
                    'PrepTime', 'DietaryInfo', 'SeasonalTags', 'PopularityScore')

    def get_Ingredients(self, obj):
        return list(obj.Ingredients.values_list("Name", flat=True))




class RecipeVersionsSerializer(serializers.ModelSerializer):
    RecipeID = serializers.UUIDField(source="Recipe.RecipeID", read_only=True)
    Author = serializers.UUIDField(source="Author.id", read_only=True)

    class Meta:
        model = RecipeVersions
        fields = ('RecipeID', 'VersionNumber', 'Author', 'Edits')




class CommentsSerializer(serializers.ModelSerializer):
    RecipeID = serializers.UUIDField(source="Recipe.RecipeID", read_only=True)
    UserID = serializers.UUIDField(source="UserID.id", read_only=True)

    class Meta:
        model = Comments
        fields = ('RecipeID', 'UserID', 'Content', 'CreatedAt')




class RecipeIngredientsSerializer(serializers.ModelSerializer):
    RecipeId = serializers.UUIDField(source="Recipe.RecipeID", read_only=True)
    IngredientName = serializers.UUIDField(source="IngredientName.Name")
    class Meta:
        model = RecipeIngredients
        fields = ('RecipeId', 'IngredientName', 'Quantity')




class RecipeNutritionSerializer(serializers.ModelSerializer):
    RecipeId = serializers.UUIDField(source="Recipe.RecipeID", read_only=True)

    class Meta:
        model = RecipeNutrition
        fields = ('__all__')
