from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class RareUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    bio = models.CharField(max_length=500)
    display_name = models.CharField(max_length=25, null=True)
    profile_image_url = models.ImageField(blank=True)
    class Meta:
        ordering = ["display_name"]
