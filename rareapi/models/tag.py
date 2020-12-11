from django.db import models


class Tag(models.Model):
    label = models.CharField(max_length=25)
    class Meta:
        ordering = ["label"]