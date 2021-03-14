from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def save_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Profile.objects.get(pk=instance.pk).image
        except Profile.DoesNotExist:
            return
        else:
            new_image = instance.image
            if old_image and old_image.url != new_image.url:
                old_image.delete(save=False)
