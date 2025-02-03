from rest_framework import serializers
from .models import User, Profile, USER_TYPE_CHOICES, DIETARY_TYPE_CHOICES

class UserRegistrationSerializer(serializers.ModelSerializer):
  """
    The UserRegistrationSerializer class is used to serialize user registration data.
    It ensures that the user provides an email, username, password, and confirmation of the password.
  """
  password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
  confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

  class Meta:
    model = User
    fields = ('email', 'username', 'password', 'confirm_password')
    extra_kwargs = {
      'email': {'required': True},
      'username': {'required': True},
    }

  def validate(self, data):
    if data['password'] != data['confirm_password']:
      raise serializers.ValidationError({'password': 'Passwords must match.'})
    return data
  
  def create(self, validated_data):
    del validated_data['confirm_password']
    return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
  """
    This serializer is responsible for handling the creation and updating of user profiles.
    It includes fields for personal information, user type, dietary restrictions, and more.
  """
  user_type_choice = serializers.ChoiceField(choices=USER_TYPE_CHOICES)
  dietary_restrictions_choice = serializers.ListField(
    child=serializers.ChoiceField(choices=DIETARY_TYPE_CHOICES),
    required=False,
    allow_null=True
  )

  class Meta:
    model = Profile
    fields = ('first_name', 'last_name', 'phone', 'profile_picture', 'user_type', 'languages', 'country', 'dietary_restrictions')
    extra_kwargs = {
      'phone': {'required': False},
      'profile_picture': {'required': False},
      'languages': {'required': False},
      'country': {'required': True},
    }

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
