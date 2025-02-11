from django.db.models.signals import post_save
from django.dispatch import receiver
from . import models

@receiver(post_save, sender=models.RecipeComments)
def auto_create_notification(sender, instance, created, **kwargs):
    if created:
        recipe = instance.Recipe
        user = recipe.User

        # if user.profile.notify_comment:  # add nofications preferences checking
        models.Notification.objects.create(User=user, content=f"New Comment on {recipe.Name}", link=f"/recipes/{recipe.RecipeID}")


@receiver(post_save, sender=models.RecipeUpdateRequests)
def auto_create_notification(sender, instance, created, **kwargs):
    if created:
        recipe = instance.Recipe
        user = recipe.User

        # if user.profile.notify_update_request:  # add nofications preferences checking
        message = f"New Update Request on {recipe.Name}"
        api_link = f"/recipes/{recipe.RecipeID}/update_requests/{instance.RequestID}/"
        
        models.Notification.objects.create(User=user, content=message, link=api_link)

