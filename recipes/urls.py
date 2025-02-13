from django.urls import path
from .views import RecipeListCreate, RecipeDetail, IngredientListCreate, IngredientDetail


urlpatterns = [
    path('api/recipes/', RecipeListCreate.as_view(), name="recipe-list-create"),
    path('api/recipes/<str:id>/', RecipeDetail.as_view(), name="recipe-detail"),
    path('api/ingredients/', IngredientListCreate.as_view(), name="ingredient-list-create"),
    path('api/ingredients/<str:name>/', IngredientDetail.as_view(), name="ingredient-detail")
]
