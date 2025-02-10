from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.postgres.search import TrigramSimilarity, SearchQuery, SearchVector, SearchRank
from django.db.models import Q, F
from recipes.models import Recipe, Ingredient
from .serializers import RecipeSearchSerializer

# Create your views here.

SIMILARITY_THRESHOLD = 0.3
def recipe_search(q):
    # A Combination of Fuzzy Search and Full-text Search
    # note: fuzzy search requires pg_trgm extention to be enabled in the postgres db
    search_vector = SearchVector('Title', 'Description')
    search_query = SearchQuery(q)

    queryset = Recipe.objects.annotate(
    similarity=TrigramSimilarity('Title', q),
    search=search_vector,)

    conditions = Q(similarity__gt=SIMILARITY_THRESHOLD) | Q(search=search_query) | Q(Keywords__icontains=q)
    conditions |= Q(Ingredients__Name__icontains=q)

    rank = SearchRank(search_vector, search_query)
    queryset = queryset.annotate(rank=rank, combined_rank=F('similarity') + F('rank'))
    
    return queryset.filter(conditions).distinct().order_by('-similarity')



class SearchAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.GET.get('q', '').strip()
        serializer = RecipeSearchSerializer(recipe_search(query), many=True)
        return Response(serializer.data)
