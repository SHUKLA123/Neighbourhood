from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import tweet9

@receiver(post_save,sender = User)
def create_Profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save,sender = User)
def save_Profile(sender, instance, **kwargs):
    instance.Profile.save()

@receiver(m2m_changed, sender=tweet9.users_like.through)
def users_like_changed(sender, instance, **kwargs):
	instance.total_likes = instance.users_like.count()
	instance.save()
