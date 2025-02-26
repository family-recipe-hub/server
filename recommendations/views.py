from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import update_recipe_likes, compute_trending_qs
from .serializers import TrendingRecipeSerializer

# Create your views here.
    
class TrendingAPIView(generics.ListAPIView):
    def get_queryset(self):
        return compute_trending_qs()
    
    def get(self, request):
        qs = self.get_queryset()
        serializer = TrendingRecipeSerializer(qs, many=True)
        return Response(serializer.data)
        