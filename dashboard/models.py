from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class TwitterUser(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.name
