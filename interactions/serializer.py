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


