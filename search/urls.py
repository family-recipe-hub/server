from django.urls import path
from rest_framework import routers
from .views import SearchAPIView

urlpatterns = [
    path('api/search/', SearchAPIView.as_view(), name='search-api'),
    
   ]   