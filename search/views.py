from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.search import TrigramSimilarity, SearchQuery, SearchVector, SearchRank
from recipes.models import Recipe, Ingredient
from .serializers import RecipeSearchSerializer
# Create your views here.


def recipe_search(q):
    # A Combination of Fuzzy Search and Full-text Search
    # note: fuzzy search requires pg_trgm extention to be enabled in the postgres db
    
    results_fuzzy_title = Recipe.objects.annotate(similarity=TrigramSimilarity('title', q)).filter(similarity__gt=0.3).order_by('-similarity')

    search_vector = SearchVector('title', 'description')
    search_query = SearchQuery(q)
    results_full_text = Recipe.objects.annotate(search_column = search_vector).filter(search_column=search_query)

    result = results_fuzzy_title | results_full_text
    matching_ingredients = Ingredient.objects.filter(name__icontains=q)
    
    if matching_ingredients.exists():
        result = result | Recipe.objects.filter(ingredients__in=matching_ingredients)
        result = result.distinct()
    
    return result



class SearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        serializer = RecipeSearchSerializer(recipe_search(query), many=True)
        return Response(serializer.data)
