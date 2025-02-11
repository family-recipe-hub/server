from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import http_date
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer, ProfileSerializer
from .models import Profile
from django.shortcuts import get_object_or_404

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
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response({
                'user': UserProfileSerializer(user).data,
                'message': 'Login successful',
                'access_token': access_token,
            })
            
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
                    'access_token': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,  # HTTP 200 OK status code.
            )

            response.set_cookie(
                'refresh_token',
                str(refresh),
                httponly=True,
                samesite='Lax',
                secure=False,
                max_age=86400,
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the POST request for user logout.

        Expects the refresh token in cookies.
        - The provided refresh token is blacklisted to invalidate it.
        - Returns a 205 status code on successful logout with a message.
        - Returns a 400 status code if the request is invalid or an error occurs.

        Args:
            request (Request): The Django REST framework request object.

        Returns:
            Response: A Django REST framework response object with a success or error message.
        """
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

                response = Response(
                    {"message": "Logout successful. Your session has been cleared."}, 
                    status=status.HTTP_205_RESET_CONTENT
                )
                response.delete_cookie('refresh_token')
                return response

            return Response(
                {"error": "No refresh token found. You might already be logged out."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": f"An error occurred while logging out: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(APIView):
    """
    API View for managing user profiles.
    
    Supports CRUD operations for authenticated users' profiles:
    - CREATE: Create a new profile for the authenticated user
    - READ: Retrieve the authenticated user's profile
    - UPDATE: Update the authenticated user's profile
    - DELETE: Delete the authenticated user's profile
    
    Endpoint: `/api/profile/`
    Permissions: Requires authentication
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a new profile for the authenticated user."""
        if hasattr(request.user, 'profile'):
            return Response(
                {'error': 'Profile already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """Retrieve the authenticated user's profile."""
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        """Update the authenticated user's profile."""
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Delete the authenticated user's profile."""
        profile = get_object_or_404(Profile, user=request.user)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)