from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class RareUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    bio = models.TextField()
    profile_image_url = models.ImageField(blank=True)
    created_on = models.DateField()
    active = models.BooleanField()
