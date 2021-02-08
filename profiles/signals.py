from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


from .models import *


@receiver(post_save, sender=User)
def postSaveCreateProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def postSaveAddFriend(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.reciever
    if instance.status == 'accepted':
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()


@receiver(pre_delete, sender=Relationship)
def preDeleteFriend(sender, instance, **kwargs):
    sender_ = instance.sender
    reciever_ = instance.reciever
    sender_.friends.remove(reciever_.user)
    reciever_.friends.remove(sender_.user)
    sender_.save()
    reciever_.save()
