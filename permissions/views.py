from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth.jwt_auth import JWTAuthentication
from .models import UserRolesPermissions, Role, User
from django.shortcuts import get_object_or_404


# class AssignRolePermissionsView(APIView):
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
    
#         is_admin = request.user.is_staff or request.user.is_superuser
#         if not is_admin:        
#             return Response(
#                 {"error": "You do not have permission to assign roles."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         user_id = request.data.get("user_id")
#         role_id = request.data.get("role_id")
#         permissions = request.data.get("permissions", {})

#         user = get_object_or_404(User, id=user_id)
#         role = get_object_or_404(Role, id=role_id)

#         # Create or update the UserRolesPermissions entry
#         user_role, created = UserRolesPermissions.objects.update_or_create(
#             user=user,
#             role=role,
#             defaults={
#                 "can_create_task": permissions.get("can_create_task", False),
#                 "can_view_task": permissions.get("can_view_task", False),
#                 "can_update_task": permissions.get("can_update_task", False),
#                 "can_delete_task": permissions.get("can_delete_task", False),
#                 "can_assign_team": permissions.get("can_assign_team", False),
#             }
#         )

#         return Response(
#             {"message": "Permissions assigned successfully!"},
#             status=status.HTTP_200_OK
        # )
        
class AssignRoleView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"error": "Only admins can assign roles."}, status=403)

        user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")

        user = get_object_or_404(User, id=user_id)
        role = get_object_or_404(Role, id=role_id)

        user_role_perm, _ = UserRolesPermissions.objects.get_or_create(user=user)
        user_role_perm.role = role
        user_role_perm.save()

        return Response({"message": "Role assigned successfully."}, status=200)

class AssignPermissionsView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if not request.user.is_superuser and not request.user.is_staff:
            return Response({"error": "Only admins can update permissions."}, status=403)

        user_id = request.data.get("user_id")
        permissions = request.data.get("permissions", {})

        user = get_object_or_404(User, id=user_id)
        user_role_perm = UserRolesPermissions.objects.filter(user=user).first()

        if not user_role_perm:
            return Response({"error": "User does not have a role assigned yet."}, status=400)

        # Update permissions
        user_role_perm.can_create_task = permissions.get("can_create_task", False)
        user_role_perm.can_view_task = permissions.get("can_view_task", False)
        user_role_perm.can_update_task = permissions.get("can_update_task", False)
        user_role_perm.can_delete_task = permissions.get("can_delete_task", False)
        user_role_perm.can_assign_team = permissions.get("can_assign_team", False)
        user_role_perm.save()

        return Response({"message": "Permissions updated successfully."}, status=200)


class CreateRoleView(APIView):
    def post(self, request):
        is_admin = request.user.is_staff or request.user.is_superuser
        if not is_admin:        
            return Response(
                {"error": "You do not have permission to create roles."},
                status=status.HTTP_403_FORBIDDEN
            )

        name = request.data.get("name")

        if not name:
            return Response(
                {"error": "Role name is required!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        role, created = Role.objects.get_or_create(name=name)

        if created:
            return Response(
                {"message": "Role created successfully!"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Role with this name already exists!"},
                status=status.HTTP_400_BAD_REQUEST
            )