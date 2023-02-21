from django.db.models.signals import post_save, post_delete
from .models import Profile
from django.contrib.auth.models import User


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        profile.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()

    except:
        pass


post_save.connect(createProfile, sender=User)

post_delete.connect(deleteUser, sender=Profile)
