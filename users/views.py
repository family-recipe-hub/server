from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserProfileSerializer

class UserRegistrationView(APIView):
    """
    API View for user registration.

    This view allows new users to register by providing necessary details such as
    username, email, password, etc. Upon successful registration, the user is saved
    to the database, and a JWT (JSON Web Token) is generated for authentication.

    Endpoint: `/api/register/`
    Method: POST
    Permissions: AllowAny (No authentication required)
    """

    # Allow any user (authenticated or not) to access this endpoint.
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handles the POST request for user registration.

        Args:
            request (Request): The HTTP request object containing user registration data.

        Returns:
            Response: A JSON response containing:
                - User profile data (if registration is successful).
                - JWT tokens (refresh and access tokens) for authentication.
                - HTTP status code:
                    - 201 Created: If registration is successful.
                    - 400 Bad Request: If the provided data is invalid.
        """
        # Initialize the serializer with the data from the request.
        serializer = UserRegistrationSerializer(data=request.data)

        # Validate the serializer data.
        if serializer.is_valid():
            # Save the user to the database.
            user = serializer.save()

            # Generate JWT tokens for the newly registered user.
            refresh = RefreshToken.for_user(user)

            # Return a response with the user's profile data and JWT tokens.
            return Response(
                {
                    'user': UserProfileSerializer(user, context={'request': request}).data,
                    'refresh': str(refresh),  # Refresh token for obtaining new access tokens.
                    'access': str(refresh.access_token),  # Access token for authentication.
                },
                status=status.HTTP_201_CREATED,  # HTTP 201 Created status code.
            )

        # If the data is invalid, return the errors with a 400 Bad Request status code.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)