from django.db import models
from django.utils import timezone
from django.db.models.deletion import CASCADE

class Subscription(models.Model):
    created_on = models.DateTimeField(default=timezone.now)
    ended_on = models.DateTimeField(blank=True)
    follower_id = models.ForeignKey("RareUser", 
        on_delete=CASCADE,
        related_name="follower_subscriptions",
        related_query_name="follower_subscription"
    )
    author_id = models.ForeignKey("RareUser",
        on_delete=CASCADE,
        related_name="author_subscriptions",
        related_query_name="author_subscription"
    )
