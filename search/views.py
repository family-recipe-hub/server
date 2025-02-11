from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.postgres.search import TrigramSimilarity, SearchQuery, SearchVector, SearchRank
from django.db.models import Q, F
from recipes.models import Recipe
from .serializers import RecipeSearchSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
# Create your views here.

SIMILARITY_THRESHOLD = 0.3
def recipe_search(q, filtered_queryset):
    # A Combination of Fuzzy Search and Full-text Search
    # note: fuzzy search requires pg_trgm extention to be enabled in the postgres db
    search_vector = SearchVector('Title', 'Description')
    search_query = SearchQuery(q)

    queryset = filtered_queryset.annotate(
    similarity=TrigramSimilarity('Title', q),
    search=search_vector,)

    conditions = Q(similarity__gt=SIMILARITY_THRESHOLD) | Q(search=search_query) | Q(Keywords__icontains=q) | Q(Category__icontains=q)
    conditions |= Q(Ingredients__Name__icontains=q)

    rank = SearchRank(search_vector, search_query)
    queryset = queryset.annotate(rank=rank, combined_rank=F('similarity') + F('rank'))
    
    return queryset.filter(conditions).distinct().order_by('-similarity')



class SearchAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSearchSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get(self, request):
        query = request.GET.get('q', '').split('&')
        query = query[0]
        # apply filtering to Recipe Model
        filtered_queryset = self.filter_queryset(self.get_queryset())
        # Serialize a search on the filtered data
        serializer = RecipeSearchSerializer(recipe_search(query, filtered_queryset), many=True)
        return Response(serializer.data)
