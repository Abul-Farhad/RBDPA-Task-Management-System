from rest_framework import serializers
from .models import Role
from accounts.models import CustomUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

