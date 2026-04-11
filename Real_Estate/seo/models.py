from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class LocationSEO(models.Model):
    key = models.CharField(max_length=180, unique=True)
    pagetype = models.CharField(max_length=30)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    primary_keyword = models.CharField(max_length=150, blank=True)
    secondary_keywords = models.CharField(max_length=255, blank=True)
    intro_html = models.TextField(blank=True)
    schema_json = models.TextField(blank=True)
    noindex = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.key} ({self.pagetype})"
