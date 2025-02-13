from django.shortcuts import get_object_or_404
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from django.http import Http404, HttpResponse
from .models import Recipe, Ingredient
from rest_framework.permissions import IsAuthenticated
from .serializers import RecipeSerializer, IngredientSerializer
from users.models import User

# Recipes CRUD operations


class RecipeListCreate(APIView):


    # permission_classes = [IsAuthenticated]

    def get(self, request):
        recipe = RecipeSerializer(Recipe.objects.all(), many=True)
        return Response(recipe.data)
    
    def post(self, request):
        recipe = RecipeSerializer(data=request.data, context={'request': request})

        if recipe.is_valid() :
            recipe.save()
            return Response(recipe.data, status=status.HTTP_201_CREATED)
        return Response(recipe.errors, status=status.HTTP_400_BAD_REQUEST)
        

class RecipeDetail(APIView):
    # permission_classes = [IsAuthenticated]


    def get_object(self, pk):
        try :
            return get_object_or_404(Recipe, pk=pk)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, id):
        recipe = RecipeSerializer(self.get_object(id))
        return Response(recipe.data)
    
    def put(self, request, id):
        recipe = RecipeSerializer(self.get_object(id), data = request.data, partial=True)
        if recipe.is_valid() : 
            recipe.save()
            return Response(recipe.data)
        else:
            return Response(recipe.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        recipe = self.get_object(id)
        if request.user != recipe.Owner:
            return HttpResponse(status=status.HTTP_403_FORBIDDEN)
        recipe.delete()
        return Response(status=status.HTTP_200_OK)

# ===================================================

# Ingredients CRUD operations

class IngredientListCreate(APIView):

    # permission_classes = [IsAuthenticated]

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

    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try :
            return get_object_or_404(Ingredient, Name=pk)
        except Ingredient.DoesNotExist:
            raise Http404

    def get(self, request, name):
        # print(name)
        # name = name.capitalize()
        # print(name)
        ingredient = self.get_object(name)
        print(ingredient)
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)
    
    def put(self, request, name):
        ingredient = IngredientSerializer(self.get_object(name), data = request.data, partial=True)
        if ingredient.is_valid() :  
            ingredient.save()
            return Response(ingredient.data)
        return Response(ingredient.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, name): 
        print(name) 
        ingredient = self.get_object(pk=name)
        print(ingredient)
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
