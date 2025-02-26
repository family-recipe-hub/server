from django.urls import path
from .views import TrendingAPIView

urlpatterns = [
    path('api/trending/', TrendingAPIView.as_view(), name='trending'),
]