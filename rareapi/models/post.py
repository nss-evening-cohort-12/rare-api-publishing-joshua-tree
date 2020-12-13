from django.db import models
from django.db.models.expressions import Case
from django.utils import timezone
from django.conf import settings
from django.db.models.deletion import CASCADE

class Post(models.Model):
    title = models.CharField(max_length=50)
    publication_date = models.DateField(default=timezone.now)
    image_url = models.ImageField(blank=True)
    content = models.CharField(max_length=2000)
    approved = models.BooleanField()
    rare_user = models.ForeignKey("RareUser", 
        on_delete=CASCADE,
        related_name="posts",
        related_query_name="post"
    )
    category = models.ForeignKey("Category",
        on_delete=CASCADE,
        related_name="posts",
        related_query_name="post"
    )
