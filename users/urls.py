from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserLogoutView,
    RefreshTokenView,
    TokenVerifyView,
    VerifyEmailView,
    ResendVerificationEmailView,
)

urlpatterns = [
    # Authentication URLs
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path(
        "verify-email/<uidb64>/<token>/", VerifyEmailView.as_view(), name="verify_email"
    ),
    path(
        "resend-verification/",
        ResendVerificationEmailView.as_view(),
        name="resend_verification_email",
    ),
    # JWT Token URLs
    path("token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
