from django.db import models
from accounts.models import CustomUser

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, related_name="assigned_tasks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
