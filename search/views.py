from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.postgres.search import TrigramSimilarity, SearchQuery, SearchVector, SearchRank
from django.db.models import Q, F, Case, When, IntegerField, Value
from recipes.models import Recipe
from .serializers import RecipeSearchSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilter
# Create your views here.

SIMILARITY_THRESHOLD = 0.01

def recipe_search(q, filtered_queryset):
    # A Combination of Fuzzy Search and Full-text Search
    # note: fuzzy search requires pg_trgm extention to be enabled in the postgres db
    q_list = q.split(' ')
   
    search_vector = SearchVector('Title', 'Description', weight='A')  # Adjust fields as needed
    search_query_obj = SearchQuery(q)
    search_rank = SearchRank(search_vector, search_query_obj)
    queryset = filtered_queryset.annotate(
    similarity_title=TrigramSimilarity('Title', q),similarity_desc=TrigramSimilarity('Description', q),
    search_vector=search_vector, search_rank=search_rank
    )

    conditions = (
        Q(similarity_title__gt=SIMILARITY_THRESHOLD) | 
        Q(similarity_desc__gt=SIMILARITY_THRESHOLD) | 
        Q(Keywords__overlap=q_list) | 
        Q(Category__icontains=q) | 
        Q(DietaryInfo__overlap=q_list) | 
        Q(SeasonalTags__overlap=q_list) | 
        Q(Difficulty__icontains=q)
    )

    rank = Case(
        When(similarity_title__gt=SIMILARITY_THRESHOLD, then=Value(10)),  # Higher weight for similarity
        When(similarity_desc__gt=SIMILARITY_THRESHOLD, then=Value(10)),
        When(Keywords__overlap=q_list, then=Value(6)),  # Lower weight for tag overlap
        When(Category__icontains=q, then=Value(4)),
        When(DietaryInfo__overlap=q_list, then=Value(4)),
        When(SeasonalTags__overlap=q_list, then=Value(4)),
        When(Difficulty__icontains=q, then=Value(2)),  # Lowest weight for difficulty
        
        default=Value(0),
        output_field=IntegerField(),
    )
    
    return queryset.annotate(rank=rank + search_rank).filter(conditions | Q(search_vector=search_query_obj)).order_by('-rank').distinct() 



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
