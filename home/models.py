from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    train = models.CharField(max_length=1024, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    # birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username + ', Trainings: ' + str(self.train != '')

    def has_train(self):
        return self.train != ''


class Room(models.Model):
    place = models.CharField(max_length=100)

    def __str__(self):
        return self.place


# MODEL
class Node(models.Model):
    camera = models.IntegerField()
    service = models.CharField(max_length=10)