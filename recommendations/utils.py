from django.db.models import Count, IntegerField, F, ExpressionWrapper, FloatField, Subquery, OuterRef
from recipes.models import Recipe
from rating.models import Rating

TRENDING_WEIGHTS = {
    'cuurent_likes': 0.2,
    'velocity': 0.7,
}

def compute_trending_qs():
    """
    Annotaes the queryset with trending score and returns it. In Descending order of score.
    """
    ratings_now = Rating.objects.filter(stars__gte=4, recipe_id=OuterRef('pk')).values('recipe_id').annotate(
        count=Count('recipe_id')
    ).values('count')
    recipes = Recipe.objects.annotate(
        diff=ExpressionWrapper(
            Subquery(ratings_now) - F('trends__last_like_count'),
            output_field=IntegerField()
        ),
        score=ExpressionWrapper(((F('diff')) * TRENDING_WEIGHTS['velocity'] )+ Subquery(ratings_now)* TRENDING_WEIGHTS['cuurent_likes'], output_field=FloatField())
     
    )
    return recipes.order_by('-score')


def update_recipe_likes():
    """
    Updates the RecipeTrendalytics model with the latest like count.
    """
    #This Function should be periodically called every 3 days.
    recipes = Recipe.objects.all()
    for recipe in recipes:
        ratings = Rating.objects.filter(recipe=recipe, stars__gte=4).count()
        recipe.trends.last_like_count = ratings
        recipe.trends.save()
        