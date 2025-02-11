from django.urls import path
from . import views

urlpatterns = [
    path('recipes/<int:recipe_id>/comments/create/', views.CreateRecipeCommentsAPIView.as_view(), name='create_comment'),
    path('recipes/<int:recipe_id>/comments/', views.RecipeCommentsListAPIView.as_view(), name='list_comments'),
    path('recipes/<int:recipe_id>/comments/<int:comment_id>/', views.RecipeCommentsDestroyUpdateAPIView.as_view(), name='comment'),
    
    path('recipes/<int:recipe_id>/update_requests/create/', views.CreateRecipeUpdateRequestsAPIView.as_view(), name='create_update_request'),
    path('recipes/<int:recipe_id>/update_requests/', views.RecipeUpdateRequestsListAPIView.as_view(), name='list_update_requests'),
    path('recipes/<int:recipe_id>/update_requests/<int:request_id>/', views.RecipeUpdateRequestsDestroyUpdateAPIView.as_view(), name='update_request'),
    
    path('playlists/create/', views.CreatePlaylistAPIView.as_view(), name='create_playlist'),
    path('playlists/', views.PlaylistListAPIView.as_view(), name='list_playlists'),
    path('playlists/<int:playlist_id>/', views.PlaylistDestroyUpdateAPIView.as_view(), name='playlist'),
    
    path('playlists/<int:playlist_id>/favorites/create/', views.CreateFavoriteAPIView.as_view(), name='create_favorite'),
    path('playlists/<int:playlist_id>/favorites/', views.FavoriteListAPIView.as_view(), name='list_favorites'),
    path('playlists/<int:playlist_id>/favorites/<int:favorite_id>/', views.FavoriteDestroyUpdateAPIView.as_view(), name='favorite'),
    
    path('notifications/', views.NotificationListAPIView.as_view(), name='list_notifications'),
    path('notifications/<int:notification_id>/', views.NotificationUpdateAPIView.as_view(), name='update_notification'),
]

