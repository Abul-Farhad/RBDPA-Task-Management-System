from rest_framework import serializers
from .models import Role, Permission, UserRolePermission
from accounts.models import CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class UserRolePermissionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, required=False)

    class Meta:
        model = UserRolePermission
        fields = ['user', 'role', 'permissions']
    