from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
    ]
    
    title = models.CharField(max_length=255)
    time_required = models.CharField(max_length=100, blank=True)
    assigned_to = models.CharField(max_length=100, default='Unassigned', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_time = models.DateTimeField(null=True, blank=True)
    overtime_hours = models.IntegerField(default=0, help_text="Additional hours if needed")
    overtime_minutes = models.IntegerField(default=0, help_text="Additional minutes if needed")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def effective_due_time(self):
        """Calculate due time including overtime"""
        if not self.due_time:
            return None
        
        overtime_delta = timedelta(hours=self.overtime_hours, minutes=self.overtime_minutes)
        return self.due_time + overtime_delta

    @property
    def is_overdue(self):
        """Check if task is overdue based on effective due time"""
        if not self.effective_due_time:
            return False
        return timezone.now() > self.effective_due_time and self.status != 'completed'

    def update_status_if_overdue(self):
        """Auto-update status to overdue if past due time"""
        if self.is_overdue and self.status == 'pending':
            self.status = 'overdue'
            self.save(update_fields=['status', 'updated'])
            return True
        return False

    class Meta:
        ordering = ['-created']
