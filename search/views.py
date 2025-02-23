from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.postgres.search import TrigramSimilarity, SearchQuery, SearchVector, SearchRank
from django.db.models import Q, F, Case, When, IntegerField, Value, FloatField
from recipes.models import Recipe
from .serializers import RecipeSearchSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from .filters import RecipeFilter
from .pagination import SearchLimitOffsetPagination
# Create your views here.

SIMILARITY_THRESHOLD = 0.3
RANK_THRESHOLD = 0.008
WEIGHTS = {'keyword_weight': 0.03, 
           'category_weight': 0.03,
           'DietartInfo_weight': 0.04,
           'SeasonalTags_weight': 0.011,
           'Ingredients_weight': 0.03
           }



def recipe_search(q, filtered_queryset):
    # A Combination of Fuzzy Search and Full-text Search
    # note: fuzzy search requires pg_trgm extention to be enabled in the postgres db
    q_list = q.split(' ')
   
    search_vector = SearchVector('Title', 'Description')  # Adjust fields as needed
    search_query_obj = SearchQuery(q)
    search_rank = SearchRank(search_vector, search_query_obj)
    queryset = filtered_queryset.annotate(
    similarity_title=TrigramSimilarity('Title', q),similarity_desc=TrigramSimilarity('Description', q),
    search_vector=search_vector, search_rank=search_rank
    )

    conditions = (
        Q(similarity_title__gte=SIMILARITY_THRESHOLD) | 
        Q(similarity_desc__gte=SIMILARITY_THRESHOLD) | 
        Q(Keywords__overlap=q_list) | 
        Q(Category__icontains=q) | 
        Q(DietaryInfo__overlap=q_list) | 
        Q(SeasonalTags__overlap=q_list) |   
        Q(Difficulty__icontains=q) |
        Q(Ingredients__Name__icontains=q)
    )

    #rank = Case(
    #    When(similarity_title__gt=SIMILARITY_THRESHOLD, then=Value(5)),  # Higher weight for similarity
    #    When(similarity_desc__gt=SIMILARITY_THRESHOLD, then=Value(5)),
    #    When(Keywords__overlap=q_list, then=Value(4)),  # Lower weight for tag overlap
    #    When(Category__icontains=q, then=Value(4)),
    #    When(DietaryInfo__overlap=q_list, then=Value(4)),
    #    When(SeasonalTags__overlap=q_list, then=Value(4)),
    #    When(Difficulty__icontains=q, then=Value(2)),  # Lowest weight for difficulty
    #    When(Ingredients__Name__icontains=q, then=Value(5)),
    #    default=Value(0),
    #    output_field=FloatField(),
    #)

    rank = (
    Case(
        When(similarity_title__gte=SIMILARITY_THRESHOLD, then=Value(0.05)),
        default=Value(0),
        output_field=FloatField()
    ) +
    Case(
        When(similarity_desc__gte=SIMILARITY_THRESHOLD, then=Value(0.04)),
        default=Value(0),
        output_field=FloatField()
    ) +
   
    Case(
        When(Keywords__overlap=q_list, then=Value(0.04)),
        default=Value(0),
        output_field=FloatField()
    ) +
    Case(
        When(Category__icontains=q, then=Value(0.03)),
        default=Value(0),
        output_field=FloatField()
    ) +
    Case(
        When(DietaryInfo__overlap=q_list, then=Value(0.04)),
        default=Value(0),
        output_field=FloatField()
    ) +
    Case(
        When(SeasonalTags__overlap=q_list, then=Value(0.011)),
        default=Value(0),
        output_field=FloatField()
    ) +
    Case(
        When(Difficulty__icontains=q, then=Value(0.01)),
        default=Value(0),
        output_field=FloatField()
    ) + Case(
        When(Ingredients__Name__icontains=q, then=Value(0.04)),
        default=Value(0),
        output_field=FloatField()
    )
)
    print(queryset.annotate(c_rank=rank + search_rank).order_by('-c_rank').values_list('Title', 'c_rank')[:10])
    return queryset.annotate(rank=rank + search_rank).order_by('-rank').filter(rank__gte=RANK_THRESHOLD).distinct()



class SearchAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSearchSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = SearchLimitOffsetPagination

    def get(self, request):
        query = request.GET.get('q', '').split('&')
        query = query[0]
        # apply filtering to Recipe Model
        filtered_queryset = self.filter_queryset(self.get_queryset())
        # Serialize a search on the filtered data 
        paginator_class = self.pagination_class()
        paginated_request = paginator_class.paginate_queryset(recipe_search(query, filtered_queryset), request)
        serializer = RecipeSearchSerializer(paginated_request, many=True)
       

        if not serializer.data:
            return JsonResponse({'results': 'nothing matches this query'})
        return Response(serializer.data)
