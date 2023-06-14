from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile, CookerRating

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user = UserProfile(user=instance)
        user.save()

    if created and instance.is_cooker:
        mark = CookerRating(cooker=instance)
        mark.save()
