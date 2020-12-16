from django.db import models
from django.db.models.deletion import CASCADE

class Comment(models.Model):
  post = models.ForeignKey("Post", on_delete=CASCADE, related_name="comments", related_query_name="comment")
  author = models.ForeignKey("RareUser", on_delete=CASCADE, related_name="comments", related_query_name="comment")
  content = models.CharField(max_length=500)
  subject = models.CharField(max_length=50)
  created_on = models.DateTimeField()

  class Meta:
    ordering = ["-created_on"]
