from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Link(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    hash = models.CharField('Hash', max_length=7)
    initial_url = models.URLField('URL')
    hash_alias = models.CharField('Alias', null=True, blank=True, unique=True, max_length=20)
    clicks = models.PositiveIntegerField('Clicks', default=0)
    active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField('CreatedAt', default=now)
    ttl = models.PositiveIntegerField('TTL', default=None, null=True, blank=True)

    def __str__(self):
        return self.initial_url
