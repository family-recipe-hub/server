from django_rest_framework import serializers
from .models import RecipeComments, RecipeUpdateRequests, Playlist, UserPlaylists, Favorite, Notification


class CreateRecipeCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeComments
        fields = ['Recipe', 'User', 'Content']

class RecipeCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeComments
        fields = ['CommentID', 'Recipe', 'User', 'Content', 'CreatedAt']
        read_only_fields = ['CommentID', 'Recipe', 'User', 'CreatedAt']


class CreateRecipeUpdateRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeUpdateRequests
        fields = ['Recipe', 'ProposalEdits', 'UserRequested']

class RecipeUpdateRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeUpdateRequests
        fields = ['RequestID', 'Recipe', 'ProposalEdits', 'UserRequested', 'Status']
        read_only_fields = ['RequestID', 'Recipe', 'ProposalEdits', 'UserRequested'] 

class CreatePlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['User', 'Name']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['PlaylistID', 'Name']
        read_only_fields = ['PlaylistID']

class CreateFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['Recipe', 'Ingredient', 'Playlist']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['FavoriteID', 'Recipe', 'Ingredient', 'SavedAt', 'Playlist']
        read_only_fields = __all__


class CreateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['User', 'content', 'link']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['NotificationID', 'User', 'content', 'Read', 'link', 'CreatedAt']
        read_only_fields = ['NotificationID', 'User', 'content', 'link', 'CreatedAt']

