from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
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


class UserLoginView(APIView):
    """
    API View for user login.

    This view allows users to log in by providing their email and password.
    Upon successful authentication, the user receives a JWT (JSON Web Token)
    for session management and access to protected endpoints.

    Endpoint: `/api/login/`
    Method: POST
    Permissions: AllowAny (No authentication required)
    """

    # Allow any user (authenticated or not) to access this endpoint.
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handles the POST request for user login.

        Args:
            request (Request): The HTTP request object containing user login data:
                - email (str): The user's email address.
                - password (str): The user's password.

        Returns:
            Response: A JSON response containing:
                - User profile data (if login is successful).
                - JWT tokens (refresh and access tokens) for authentication.
                - HTTP status code:
                    - 200 OK: If login is successful.
                    - 400 Bad Request: If the provided credentials are invalid.
        """
        # Extract email and password from the request data.
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using the provided credentials.
        user = authenticate(request, email=email, password=password)

        if user:
            # If authentication is successful, generate JWT tokens.
            refresh = RefreshToken.for_user(user)

            # Return the user's profile data and JWT tokens.
            return Response(
                {
                    'user': UserProfileSerializer(user).data,  # Serialized user profile data.
                    'refresh': str(refresh),  # Refresh token for obtaining new access tokens.
                    'access': str(refresh.access_token),  # Access token for authentication.
                },
                status=status.HTTP_200_OK,  # HTTP 200 OK status code.
            )

        # If authentication fails, return an error message.
        return Response(
            {'error': 'Invalid credentials'},  # Error message for invalid credentials.
            status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
        )
