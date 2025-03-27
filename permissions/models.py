from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class UserRolesPermissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    can_create_task = models.BooleanField(default=False)
    can_view_task = models.BooleanField(default=False)
    can_update_task = models.BooleanField(default=False)
    can_delete_task = models.BooleanField(default=False)
    can_assign_team = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"
