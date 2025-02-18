from rest_framework import serializers
from .models import User, Profile, USER_TYPE_CHOICES, DIETARY_TYPE_CHOICES
from .validation import EmailValidator


class UserRegistrationSerializer(serializers.ModelSerializer):
  """
    The UserRegistrationSerializer class is used to serialize user registration data.
    It ensures that the user provides an email, username, password, and confirmation of the password.
  """
  class Meta:
    model = User
    fields = ('email', 'username', 'password')
    extra_kwargs = {
      'email': {'required': True},
      'username': {'required': True},
      'password': {'write_only': True}
    }


  def create(self, validated_data):
    return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
  """
    This serializer is responsible for handling the creation and updating of user profiles.
    It includes fields for personal information, user type, dietary restrictions, and more.
  """

  class Meta:
    model = Profile
    fields = ('first_name', 'last_name', 'phone', 'profile_picture', 'user_type', 'country', 'dietary_restrictions')
    extra_kwargs = {
      'phone': {'required': False},
      'profile_picture': {'required': False},
      'languages': {'required': False},
      'country': {'required': True},
    }

    def validate(self, data):
  
      return super().validate(data)

    def create(self, validated_data):
      validated_data['user'] = self.context['request'].user
      return super().create(validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
  """
    This serializer is responsible for retrieving user details
    along with their associated profile information.
  """
  profile = ProfileSerializer()

  class Meta:
    model = User
    fields = ('id', 'email', 'username', 'profile')
