from rest_framework.permissions import BasePermission
from .models import UserRole, Role



class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        print("slkdfjsfj")
        # If superuser or staff, bypass permission check
        if request.user.is_superuser or request.user.is_staff:
            print(f"If {request.user} is superuser or staff: ", request.user.is_superuser or request.user.is_staff)  # Debugging line
            return True
        
        
        print("sdkjfsklfjsk")
        # Get the required permission codename(s)
        required_perms = getattr(view, "required_permissions", [])
        
        if not required_perms:
            return False
        print(request.user, required_perms)  # Debugging line   
        try:
            user_role = UserRole.objects.get(user=request.user)
            # print(request.user)  # Debugging line
            role = user_role.role
            # print(request.user, role)
            
        except UserRole.DoesNotExist:
            # print(request.user)  # Debugging line
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
