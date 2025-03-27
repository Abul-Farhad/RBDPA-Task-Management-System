from rest_framework.permissions import BasePermission
from .models import UserRolesPermissions

class CanCreateTaskPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            user_permissions = UserRolesPermissions.objects.get(user=request.user)
            return user_permissions.can_create_task
        except UserRolesPermissions.DoesNotExist:
            return False

class CanViewTaskPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            user_permissions = UserRolesPermissions.objects.get(user=request.user)
            return user_permissions.can_view_task
        except UserRolesPermissions.DoesNotExist:
            return False

class CanUpdateTaskPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            user_permissions = UserRolesPermissions.objects.get(user=request.user)
            return user_permissions.can_update_task
        except UserRolesPermissions.DoesNotExist:
            return False

class CanDeleteTaskPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            user_permissions = UserRolesPermissions.objects.get(user=request.user)
            return user_permissions.can_delete_task
        except UserRolesPermissions.DoesNotExist:
            return False
