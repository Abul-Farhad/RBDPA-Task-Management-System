from rest_framework.permissions import BasePermission
from .models import UserRole, Role



class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        print("HasRolePermission.has_permission called")
        # If superuser or staff, bypass permission check
        print(f"User: {request.user}")
        if request.user.is_superuser or request.user.is_staff:
            print("user is superuser or staff")
            return True
        
        
        # Get the required permission codename(s)
        required_perms = getattr(view, "required_permissions", [])
        
        if not required_perms:
            return False
        try:
            user_role = UserRole.objects.get(user=request.user)

            role = user_role.role

            
        except UserRole.DoesNotExist:

            return False
        
        # Check each permission codename
        for perm in required_perms:
            if not hasattr(role, perm) or not getattr(role, perm):
                
                return False  # Missing a required permission

        return True  # All required permissions granted



# class CanCreateTaskPermission(BasePermission):
#     def has_permission(self, request, view):
#         try:
#             if request.user.is_superuser or request.user.is_staff: 
#                 return True
#             user_permissions = UserRole.objects.get(user=request.user)
#             return user_permissions.role.can_create_task
#         except UserRole.DoesNotExist:
#             return False

# class CanViewTaskPermission(BasePermission):
#     def has_permission(self, request, view):
#         try:
#             if request.user.is_superuser or request.user.is_staff: 
#                 return True
#             user_permissions = UserRole.objects.get(user=request.user)
#             return user_permissions.role.can_view_task
#         except UserRole.DoesNotExist:
#             return False

# class CanUpdateTaskPermission(BasePermission):
#     def has_permission(self, request, view):
#         try:
#             if request.user.is_superuser or request.user.is_staff: 
#                 return True
#             user_permissions = UserRole.objects.get(user=request.user)
#             return user_permissions.role.can_update_task
#         except UserRole.DoesNotExist:
#             return False

# class CanDeleteTaskPermission(BasePermission):
#     def has_permission(self, request, view):
#         try:
#             if request.user.is_superuser or request.user.is_staff: 
#                 return True
#             user_permissions = UserRole.objects.get(user=request.user)
#             return user_permissions.role.can_delete_task
#         except UserRole.DoesNotExist:
#             return False
