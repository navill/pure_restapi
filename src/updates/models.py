from django.conf import settings
from django.contrib.gis import views
from django.db import models


def upload_update_image(instance, filename):
    return f'updates/{instance.user}/{filename}'


class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text