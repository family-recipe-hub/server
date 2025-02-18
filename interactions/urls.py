from django.urls import path
from . import views

urlpatterns = [
    path('comments/create/', views.CreateRecipeCommentsAPIView.as_view(), name='create_comment'),
    path('recipes/<str:recipe_id>/comments/', views.RecipeCommentsListAPIView.as_view(), name='list_comments'),
    path('comments/<str:comment_id>/', views.RecipeCommentsDestroyUpdateAPIView.as_view(), name='comment'),
    
    path('update_requests/create/', views.CreateRecipeUpdateRequestsAPIView.as_view(), name='create_update_request'),
    path('recipes/<str:recipe_id>/update_requests/', views.RecipeUpdateRequestsListAPIView.as_view(), name='list_update_requests'),
    path('update_requests/<str:request_id>/', views.RecipeUpdateRequestsDestroyUpdateAPIView.as_view(), name='update_request'),
    
    path('playlists/create/', views.CreatePlaylistAPIView.as_view(), name='create_playlist'),
    path('playlists/', views.PlaylistListAPIView.as_view(), name='list_playlists'),
    path('playlists/<str:playlist_id>/', views.PlaylistDestroyUpdateAPIView.as_view(), name='playlist'),
    
    path('playlists/<str:playlist_id>/favorites/', views.FavoriteListCreateAPIView.as_view(), name='list_create_favorites'),
    path('favorites/<str:favorite_id>/', views.FavoriteDestroyUpdateAPIView.as_view(), name='favorite'),
    
    path('notifications/', views.NotificationListAPIView.as_view(), name='list_notifications'),
    path('notifications/<str:notification_id>/', views.NotificationUpdateAPIView.as_view(), name='update_notification'),
]

