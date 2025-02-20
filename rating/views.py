from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from .serializers import RateSerializer
from rest_framework.response import Response
from rest_framework import status
from recipes.models import Recipe
from .models import Rating
from django.db.models import Sum
from math import floor,ceil
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AddRate(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,recipe_id):
        serializer = RateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        recipe = get_object_or_404(Recipe,RecipeID=recipe_id)

        try:
            Rating.objects.create(user = user,recipe=recipe,stars=serializer.validated_data.get('stars'))
        except:
            return Response({'error':'you cannot rate the recipe twice'},status=status.HTTP_403_FORBIDDEN)
        return Response({'message':'you have rated this recipe'},status=status.HTTP_200_OK)


class CalculateTotalStars(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
       
        sum2 = Rating.objects.aggregate(Sum('stars'))
        
        no_records = Rating.objects.count()
        result = (sum2['stars__sum'])/(5*no_records)
        print(no_records)
        final_rating=0
        if result-floor(result)>0.5:
            final_rating=ceil(result)
        else:
            final_rating=floor(result)
        return Response(final_rating,status=status.HTTP_200_OK)