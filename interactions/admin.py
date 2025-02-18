from django.contrib import admin
from . import models

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('NotificationID', 'User', 'content', 'CreatedAt')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('FavoriteID', 'Playlist', 'Recipe', 'SavedAt')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('PlaylistID', 'User', 'Name')

class RecipeUpdateRequestsAdmin(admin.ModelAdmin):
    list_display = ('RequestID', 'Recipe', 'UserRequested', 'Status')

class RecipeCommentsAdmin(admin.ModelAdmin):
    list_display = ('CommentID', 'Recipe', 'User', 'Content', 'CreatedAt')

admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.Playlist, PlaylistAdmin)
admin.site.register(models.RecipeUpdateRequests, RecipeUpdateRequestsAdmin)
admin.site.register(models.RecipeComments, RecipeCommentsAdmin)
