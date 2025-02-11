from recipes.models import Recipe
from django_filters import rest_framework as filters

class RecipeFilter(filters.FilterSet):
    class Meta:
        model = Recipe
        fields = {
            'PrepTime': ['exact', 'lt', 'gt', 'range'],
            'CookingTime': ['exact', 'lt', 'gt', 'range'],
            'rating': ['gt'],
            'Category': ['icontains', 'iexact'],
            'Difficulty': ['iexact'],
        }