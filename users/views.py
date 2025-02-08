from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.core.cache import cache

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
        print(request.data)

        # Validate the serializer data.
        if serializer.is_valid():
            # Save the user to the database.
            user = serializer.save()

            # Generate JWT tokens for the newly registered user.
            refresh = RefreshToken.for_user(user)

            # Return a response with the user's profile data and JWT tokens.
            response = Response(
                {
                    'user': UserProfileSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,  # HTTP 201 Created status code.
            )
        
            # Set cookies for JWT tokens
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            return response 

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
            response = Response(
                {
                    'user': UserProfileSerializer(user).data,  # Serialized user profile data.
                },
                status=status.HTTP_200_OK,  # HTTP 200 OK status code.
            )
        
            # Set cookies for JWT tokens
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite="Lax",
            )

            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
            )
            return response

        # If authentication fails, return an error message.
        return Response(
            {'error': 'Invalid credentials'},  # Error message for invalid credentials.
            status=status.HTTP_400_BAD_REQUEST,  # HTTP 400 Bad Request status code.
        )

class UserLogoutView(APIView):
    """
    A view to handle user logout functionality. 
    This view invalidates the provided refresh token by blacklisting it,
    ensuring the token can no longer be used to generate new access tokens.

    Requires the user to be authenticated to access this endpoint.
    """

    # Only authenticated users can access this view
    permission_classes=[IsAuthenticated]

    def post(self, request):
        """
        Handles the POST request for user logout.

        Expects a JSON payload with a `refresh_token` field.
        - The provided refresh token is blacklisted to invalidate it.
        - Returns a 205 status code on successful logout.
        - Returns a 400 status code if the request is invalid or an error occurs.

        Args:
            request (Request): The Django REST framework request object containing the refresh token.

        Returns:
            Response: A Django REST framework response object with an appropriate status code.
        """
        try:
            # Extract the refresh token from the request data.
            refresh_token = request.data["refresh_token"]
            if refresh_token:
                token = RefreshToken(refresh_token)
                # Blacklist the provided refresh token.
                token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            # Clear cookies
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)