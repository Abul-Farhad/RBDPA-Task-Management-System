from rest_framework.permissions import BasePermission
from django.urls import resolve
from .models import UserRole, Role




class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        print("HasRolePermission.has_permission called")
        print(f"User: {request.user}")

        # Bypass check for superusers or staff
        if request.user.is_superuser or request.user.is_staff:
            print("User is superuser or staff — permission granted.")
            return True

        try:
            # Get the name of the URL route (e.g., 'create-role')
            code_name = resolve(request.path).url_name
            print(f"Resolved route name (codename): {code_name}")
        except Exception as e:
            print(f"Error resolving route name: {e}")
            return False

        if not code_name:
            print("No route name assigned to this view.")
            return False

        try:
            # Get user's role and its permissions
            user_role = UserRole.objects.get(user=request.user)
            role_permissions = user_role.role.permissions  # Should be a list or dict of codenames
            print(f"User's role: {user_role.role.name}")
            print(f"Permissions for role: {role_permissions}")
        except UserRole.DoesNotExist:
            print("User has no assigned role.")
            return False

        # Check if the required codename exists in role permissions
        if code_name not in role_permissions:
            print(f"Permission '{code_name}' is NOT granted to this role.")
            return False

        print(f"Permission '{code_name}' granted.")
        return True



