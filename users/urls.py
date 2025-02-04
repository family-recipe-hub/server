from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import UserRegistrationView
urlpatterns = [
    # Authentication URLs
    path('register/', UserRegistrationView.as_view(), name='user_register'),

    #JWT Token URLs
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
