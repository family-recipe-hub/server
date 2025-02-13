from django.contrib import admin
from .models import Recipe, RecipeNutrition, RecipeVersions, Ingredient, Comments
# Register your models here.
admin.site.register(Recipe)
# admin.site.register(RecipeIngredients)
admin.site.register(RecipeNutrition)
admin.site.register(RecipeVersions)
admin.site.register(Ingredient)
admin.site.register(Comments)
