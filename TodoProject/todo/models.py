from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    time_required = models.CharField(max_length=100)  # e.g. "2 hours"
    assigned_to = models.CharField(max_length=100, default='Unassigned')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_time = models.DateTimeField(null=True, blank=True)  # new field
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



