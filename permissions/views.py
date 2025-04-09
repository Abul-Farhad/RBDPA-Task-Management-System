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

        user_role_perm, _ = UserRole.objects.get_or_create(user=user)
        user_role_perm.role = role
        user_role_perm.save()

        send_notification(user.id, f"🎉 You have been assigned the role '{role.name}'.")
        return Response({"message": "Role assigned successfully."}, status=200)


class CreateRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Role created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def patch(self, request):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response({"error": "Role ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, id=role_id)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Role updated successfully!", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
class DeleteRoleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def delete(self, request):
        role_id = request.data.get("role_id")
        if not role_id:
            return Response({"error": "Role ID is required!"}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, id=role_id)
        role.delete()
        return Response({"message": "Role deleted successfully!"}, status=status.HTTP_200_OK)
