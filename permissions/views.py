from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserRolesPermissions, Role, User
from django.shortcuts import get_object_or_404


class AssignRolePermissionsView(APIView):
    # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Check if the user is an staff or superuser
        # is_admin = request.data.get("is_staff", False) or request.data.get("is_superuser", False)
        # if not is_admin:
        #     return Response(
        #         {"error": "You do not have permission to assign roles."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")
        permissions = request.data.get("permissions", {})

        user = get_object_or_404(User, id=user_id)
        role = get_object_or_404(Role, id=role_id)

        # Create or update the UserRolesPermissions entry
        user_role, created = UserRolesPermissions.objects.update_or_create(
            user=user,
            role=role,
            defaults={
                "can_create_task": permissions.get("can_create_task", False),
                "can_view_task": permissions.get("can_view_task", False),
                "can_update_task": permissions.get("can_update_task", False),
                "can_delete_task": permissions.get("can_delete_task", False),
                "can_assign_team": permissions.get("can_assign_team", False),
            }
        )

        return Response(
            {"message": "Permissions assigned successfully!"},
            status=status.HTTP_200_OK
        )

class CreateRoleView(APIView):
    def post(self, request):
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