from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Model connected to djangos user model to extend the information
# we will get about the user
class Wanderer(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, blank=True)
    content = models.CharField(max_length=200, blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profileimage_abyxmi'
    )
    one_important_thing = models.CharField(max_length=200, blank=True)
    favorite_place = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Wanderer: {self.owner}"


# Signal receiver to reate a Wanderer object when a User is crated
def create_wanderer(sender, instance, created, **kwargs):
    if created:
        Wanderer.objects.create(owner=instance)


post_save.connect(create_wanderer, sender=User)
