from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from . import models

@receiver(post_save, sender=models.RecipeComments)
def auto_create_comment_notification(sender, instance, created, **kwargs):
    if created:
        recipe = instance.Recipe
        user = recipe.Owner
        api_link = reverse('comment', kwargs={'comment_id': instance.CommentID})
        # Try to find an existing comment notification for this recipe else create one
        notification, created_notif = models.Notification.objects.get_or_create(
            User=user,
            NotificationType='comment',
            defaults={
                'content': f"New comment on {recipe.Title}",
                'link': api_link,
                'NotificationCount': 1
            }
        )
        # If already exists, update it
        if not created_notif:
            notification.NotificationCount += 1
            notification.content = f"{notification.NotificationCount} new comments on {recipe.Title}"
            notification.CreatedAt = models.DateTimeField(auto_now=True)
            notification.save()

@receiver(post_save, sender=models.RecipeUpdateRequests)
def auto_create_update_request_notification(sender, instance, created, **kwargs):
    if created:
        recipe = instance.Recipe
        user = recipe.Owner
        api_link = reverse('update_request', kwargs={'request_id': instance.RequestID})
        # Try to find an existing update request notification for this recipe else create one
        notification, created_notif = models.Notification.objects.get_or_create(
            User=user,
            NotificationType='update_request',
            defaults={
                'content': f"New update request on {recipe.Title}",
                'link': api_link,
                'NotificationCount': 1
            }
        )
        # If already exists, update it
        if not created_notif:
            notification.NotificationCount += 1
            notification.content = f"{notification.NotificationCount} new update requests on {recipe.Title}"
            notification.CreatedAt = models.DateTimeField(auto_now=True)
            notification.save()
