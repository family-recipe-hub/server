from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializer
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class CreateRecipeCommentsAPIView(generics.CreateAPIView):
    """
    API view for creating comments on recipe.

    This view is used to create comments on a recipe.
    The user must be authenticated to create a comment.

    Endpoint: `/api/recipes/<recipe_id>/comments/create/`
    Method: POST
    Permissions: IsAuthenticated (User must be authenticated)
    """

    serializer_class = serializer.CreateRecipeCommentsSerializer
    queryset = models.RecipeComments.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

class RecipeCommentsListAPIView(generics.ListAPIView):
    """
    API view for listing recipe comments.

    This view is used to list recipe comments .
    The user must be authenticated to view comments.

    Endpoint: `/api/recipes/<recipe_id>/comments/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.RecipeCommentSerializer
    queryset = models.RecipeComments.objects.order_by('-CreatedAt')
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        return models.RecipeComments.objects.filter(Recipe=recipe_id).all()


class RecipeCommentsDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for updating and deleting comments on recipe.

    This view is used to update and delete comments on a recipe.
    The user must be authenticated to update and delete a comment.
    The user can only delete their own comments.

    Endpoint: `/api/recipes/<recipe_id>/comments/<comment_id>/`
    Method: DELETE, PUT
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.RecipeCommentSerializer
    queryset = models.RecipeComments.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_field = 'CommentID'

    def perform_destroy(self, instance):
        if instance.User == self.request.user or instance.Recipe.Owner == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this comment."},
                code=status.HTTP_403_FORBIDDEN
            )

    def perform_update(self, serializer):
        if serializer.instance.User == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this comment."},
                code=status.HTTP_403_FORBIDDEN
            )
        
class CreateRecipeUpdateRequestsAPIView(generics.CreateAPIView):
    """
    API view for creating update requests on recipe.

    This view is used to create update requests on a recipe.
    The user must be authenticated to create an update request.

    Endpoint: `/api/recipes/<recipe_id>/update_requests/create/`
    Method: POST
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.CreateRecipeUpdateRequestsSerializer
    queryset = models.RecipeUpdateRequests.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(UserRequested=self.request.user)
   
class RecipeUpdateRequestsListAPIView(generics.ListAPIView):
    """
    API view for listing recipe update requests.

    This view is used to list recipe update requests.
    The user must be authenticated to view update requests.

    Endpoint: `/api/recipes/<recipe_id>/update_requests/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.RecipeUpdateRequestSerializer
    queryset = models.RecipeUpdateRequests.objects.all()
    permission_classes = [IsAuthenticated,]
    filter_fields = ['Recipe', 'UserRequested']

class RecipeUpdateRequestsDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for updating and deleting update requests on recipe.
    
    This view is used to view, update and delete update requests on a recipe.
    The user must be authenticated to view, update and delete an update request.
    
    Endpoint: `/api/recipes/<recipe_id>/update_requests/<request_id>/`
    Method: GET, DELETE, PUT
    Permissions: IsAuthenticated (User must be authenticated)
    """

    serializer_class = serializer.RecipeUpdateRequestSerializer
    queryset = models.RecipeUpdateRequests.objects.all()
    permission_classes = [IsAuthenticated,]
    # acessing the request by the request id
    lookup_field = 'RequestID'

    def perform_destroy(self, instance):
        # checking if the user is the owner of the request
        if instance.UserRequested == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this request."},
                code=status.HTTP_403_FORBIDDEN
            )

    def perform_update(self, serializer):
        # only the user who recives the request can update the status
        if self.request.user == serializer.instance.Recipe.Owner:
            serializer.save()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this update request."},
                code=status.HTTP_403_FORBIDDEN
            )

    def get_object(self):
        # checking if the user is the owner of the request
        obj = super().get_object()
        if obj.UserRequested == self.request.user or obj.Recipe.Owner == self.request.user:
            return obj
        raise PermissionDenied(
            {"detail": "You do not have permission to view this update request."},
            code=status.HTTP_403_FORBIDDEN
        )

        
class CreatePlaylistAPIView(generics.CreateAPIView):
    """
    API view for creating a playlist.

    This view is used to create a playlist.
    The user must be authenticated to create a playlist.

    Endpoint: `/api/playlists/create/`
    Method: POST
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.CreatePlaylistSerializer
    queryset = models.Playlist.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(User=self.request.user)

class PlaylistListAPIView(generics.ListAPIView):
    """
    API view for listing playlists.

    This view is used to list playlists.
    The user must be authenticated to view playlists.

    Endpoint: `/api/playlists/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.PlaylistSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return models.Playlist.objects.filter(User=self.request.user)


class PlaylistDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for updating and deleting playlists.

    This view is used to update and delete playlists.
    The user must be authenticated to update and delete a playlist.
    The user can only delete their own playlists.

    Endpoint: `/api/playlists/<playlist_id>/`
    Method: DELETE, PUT
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.PlaylistSerializer
    queryset = models.Playlist.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_field = 'PlaylistID'

    def perform_destroy(self, instance):
        if instance.User == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to delete this playlist."},
                code=status.HTTP_403_FORBIDDEN
            )

    def perform_update(self, serializer):
        if serializer.instance.User == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this playlist."},
                code=status.HTTP_403_FORBIDDEN
            )


class CreateFavoriteAPIView(generics.CreateAPIView):
    """
    API view for creating a favorite.

    This view is used to create a favorite.
    The user must be authenticated to create a favorite.

    Endpoint: `/api/playlists/<playlist_id>/favorites/create/`
    Method: POST
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.CreateFavoriteSerializer
    queryset = models.Favorite.objects.all()
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        playlist = models.Playlist.objects.get(PlaylistID=self.kwargs.get('playlist_id'))
        # checking if the user is the owner of the playlist
        if playlist.User == self.request.user:
            serializer.save(Playlist=playlist)
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to add a favorite to this playlist."},
                code=status.HTTP_403_FORBIDDEN
            )

class FavoriteListAPIView(generics.ListAPIView):
    """
    API view for listing favorites.

    This view is used to list favorites.
    The user must be authenticated to view favorites.

    Endpoint: `/api/playlists/<playlist_id>/favorites/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.FavoriteSerializer
    permission_classes = [IsAuthenticated,]


    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')
        return models.Favorite.objects.filter(Playlist=playlist_id).all()
    

class FavoriteDestroyUpdateAPIView(APIView):
    """
    API view for updating and deleting favorites.

    This view is used to update and delete favorites.
    The user must be authenticated to update and delete a favorite.
    The user can only delete their own favorites.

    Endpoint: `/api/playlists/<playlist_id>/favorites/<favorite_id>/`
    Method: GET, DELETE
    Permissions: IsAuthenticated (User must be authenticated)
    """
    def get(self, request, favorite_id):
        favorite = models.Favorite.objects.select_related('Playlist').get(FavoriteID=favorite_id)
        if favorite.Playlist.User == request.user:
            serializer = serializer.FavoriteSerializer(favorite)
            return Response(serializer.data)
        else: 
            raise PermissionDenied(
                code=status.HTTP_403_FORBIDDEN
            )
        
    def delete(self, request, favorite_id):
        favorite = models.Favorite.objects.select_related('Playlist').get(FavoriteID=favorite_id)
        if favorite.Playlist.User == request.user:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied(
                code=status.HTTP_403_FORBIDDEN
            )
        
        
class NotificationListAPIView(generics.ListAPIView):
    """
    API view for listing notifications.

    This view is used to list notifications.
    The user must be authenticated to view notifications.

    Endpoint: `/api/notifications/`
    Method: GET
    Permissions: IsAuthenticated (User must be authenticated)
    """
    serializer_class = serializer.NotificationSerializer
    queryset = models.Notification.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return models.Notification.objects.filter(User=self.request.user).all()
    
class NotificationUpdateAPIView(generics.UpdateAPIView):
    """
    API view for updating notification status.

    This view is used to update notification status.
    The user must be authenticated to update notification status.

    Endpoint: `/api/notifications/<notification_id>/`
    """
    serializer_class = serializer.NotificationSerializer
    queryset = models.Notification.objects.all()
    permission_classes = [IsAuthenticated,]
    lookup_field = 'NotificationID'

    def perform_update(self, serializer):
        if serializer.instance.User == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(
                {"detail": "You do not have permission to update this notification."},
                code=status.HTTP_403_FORBIDDEN
            )
        
        
