from rest_framework import serializers
from .models import RecipeComments, RecipeUpdateRequests, Playlist, Favorite, Notification


class CreateRecipeCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeComments
        fields = ['Recipe', 'Content', 'User']

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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['FavoriteID', 'Recipe', 'Ingredient', 'SavedAt']
        read_only_fields = ['FavoriteID', 'SavedAt']


class CreateNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['User', 'content', 'link']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['NotificationID', 'User', 'content', 'Read', 'link', 'CreatedAt']
        read_only_fields = ['NotificationID', 'User', 'content', 'link', 'CreatedAt']