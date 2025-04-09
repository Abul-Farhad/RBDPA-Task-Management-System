from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from auth.jwt_auth import JWTAuthentication
from .models import UserRole, Role, User
from django.shortcuts import get_object_or_404
from permissions.permissions import HasRolePermission
from .serializers import RoleSerializer
from notifications.utils import send_notification

        
class AssignRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def post(self, request):
        
        user_id = request.data.get("user_id")
        role_id = request.data.get("role_id")
        
        user = get_object_or_404(User, id=user_id)
        role = get_object_or_404(Role, id=role_id)
        print(user, role)
        user_role_perm, _ = UserRole.objects.get_or_create(user=user, role=role)
        # user_role_perm.role = role
        user_role_perm.save()
        send_notification(user.id, f"🎉 You have been assigned the role '{role.name}'.")
        return Response({"message": "Role assigned successfully."}, status=200)




class CreateRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]
    def post(self, request):
 
        name = request.data.get("name")
        permissions = request.data.get("permissions", {})

        if Role.objects.filter(name=name).exists():
            return Response(
                {"error": "Role with this name already exists!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not name:
            return Response(
                {"error": "Role name is required!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        role = Role.objects.create(
            name=name,
            can_create_task=permissions.get("can_create_task", False),
            can_view_task=permissions.get("can_view_task", False),
            can_update_task=permissions.get("can_update_task", False),
            can_delete_task=permissions.get("can_delete_task", False),
            can_assign_team=permissions.get("can_assign_team", False),
        )

        serializer = RoleSerializer(role)  # Serialize the Role object
        return Response(
            {"message": "Role created successfully!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
        
class UpdateRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def patch(self, request):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {"error": "Role ID is required!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        role = get_object_or_404(Role, id=role_id)
        name = request.data.get("name")
        permissions = request.data.get("permissions", {})

        if name:
            role.name = name
        for perm, value in permissions.items():
            if hasattr(role, perm):
                setattr(role, perm, value)
            else:
                return Response(
                    {"error": f"Invalid permission: {perm}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        role.save()

        serializer = RoleSerializer(role)  # Serialize the Role object
        return Response(
            {"message": "Role updated successfully!", "data": serializer.data},
            status=status.HTTP_200_OK
        )
        
        
class DeleteRoleView(APIView):
    authentication_classed = [JWTAuthentication]
    permission_classes = [HasRolePermission]
    
    def delete(self, request):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response(
                {"error": "Role ID is required!"},
                status=status.HTTP_400_BAD_REQUEST
            )
        role = get_object_or_404(Role, id=role_id)
        role.delete()
        return Response(
            {"message": "Role deleted successfully!"},
            status=status.HTTP_200_OK
        )