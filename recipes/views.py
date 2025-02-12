from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from django.http import Http404, HttpResponse
from .models import Recipe, Ingredient
from rest_framework.permissions import IsAuthenticated
from .serializers import RecipeSerializer, IngredientSerializer

# Recipes CRUD operations


class RecipeListCreate(APIView):


    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipe = RecipeSerializer(Recipe.objects.all(), many=True)
        return Response(recipe.data)
    
    def post(self, request):
        recipe = RecipeSerializer(data=request.data)

        if recipe.is_valid() :
            recipe.save(Owner=request.user)
            return Response(recipe.data, status=status.HTTP_201_CREATED)
        return Response(recipe.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RecipeDetail(APIView):
    permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try :
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, id):
        recipe = RecipeSerializer(self.get_object(id))
        return Response(recipe.data)
    
    def put(self, request, id):
        recipe = RecipeSerializer(self.get_object(id), data = request.data)
        if recipe.is_valid() : 
            recipe.save()
            return Response(recipe.data)
        return Response(recipe.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        recipe = RecipeSerializer(self.get_object(id))
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ===================================================

# Ingredients CRUD operations

class IngredientListCreate(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        ingredient = IngredientSerializer(Ingredient.objects.all(), many=True)
        return Response(ingredient.data)
    
    def post(self, request):
        ingredient = IngredientSerializer(data=request.data)

        if ingredient.is_valid() :
            ingredient.save()
            return Response(ingredient.data, status=status.HTTP_201_CREATED)
        return Response(ingredient.errors, status=status.HTTP_400_BAD_REQUEST)
        

class IngredientDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try :
            return Ingredient.objects.get(pk=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, id):
        ingredient = IngredientSerializer(self.get_object(id))
        return Response(ingredient.data)
    
    def put(self, request, id):
        ingredient = IngredientSerializer(self.get_object(id), data = request.data)
        if ingredient.is_valid() : 
            ingredient.save()
            return Response(ingredient.data)
        return Response(ingredient.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        ingredient = IngredientSerializer(self.get_object(id))
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
