import os
from django.db import models
from django.db.models.expressions import Case
from django.utils import timezone
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

class Post(models.Model):

    def upload_to(instance, filename):
        now = timezone.now()
        base, extension = os.path.splitext(filename.lower())
        milliseconds = now.microsecond // 1000
        return f"posts/{instance.rare_user}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"
    
    title = models.CharField(max_length=50)
    publication_date = models.DateTimeField(default=timezone.now)
    image_url = models.ImageField(_("Post Image"), blank=True, upload_to=upload_to)
    content = models.CharField(max_length=2000)
    approved = models.BooleanField()
    rare_user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=CASCADE,
        related_name="posts",
        related_query_name="post"
    )
    category = models.ForeignKey("Category",
        on_delete=CASCADE,
        related_name="posts",
        related_query_name="post"
    )
    class Meta:
        ordering = ["-publication_date"]
