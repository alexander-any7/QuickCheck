from django.db import models
from django_extensions.db.models import TimeStampedModel


TYPES = ["job", "story","poll", "pollopt"]

class HackerNewsPost(TimeStampedModel, models.Model):
    post_id = models.CharField(max_length=500, unique=True)
    descendants = models.CharField(max_length=500, blank=True, null=True)
    by = models.CharField(max_length=500, blank=True, null=True)
    kids = models.TextField(max_length=500, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.PositiveIntegerField(blank=True, null=True)
    parent = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Posts'

    def __str__(self) -> str:
        return self.title



