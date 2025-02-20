from django.urls import path,include
from . import views

urlpatterns = [
    path('add_rate/<uuid:recipe_id>/',views.AddRate.as_view(),name='add_rate'),
    path('total_stars/',views.CalculateTotalStars.as_view(),name='calculate_total_stars'),

]