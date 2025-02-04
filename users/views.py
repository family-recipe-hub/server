from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserRegistrationSerializer, UserProfileSerializer

from .models import User

class UserRegistrationView(APIView):
  """
  User registration view.
  """
  # Allow any user (authenticated or not) to hit this endpoint.
  permission_classes = (AllowAny,)

  def post(self, request):
    # define the serializer with the request data
    serializer = UserRegistrationSerializer(data=request.data)
    # check if the serializer is valid
    if serializer.is_valid():
      # save the user to the database
      user = serializer.save()
      # generate a jwt token for the user
      refresh = RefreshToken.for_user(user)
      return Response({
        'user': UserProfileSerializer(user, context={'request': request}).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
      }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
