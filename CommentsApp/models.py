from __future__ import unicode_literals

from django.db import models
from GroupsApp.models import Group

class Comment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    time = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=500)
