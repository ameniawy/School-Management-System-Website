from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class user_type(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=200)


