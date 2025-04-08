from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

from auth.jwt_auth import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer
from permissions.permissions import HasRolePermission

class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]
    required_permissions = ['can_create_task']  # Specify the required permission for this view

class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]
    required_permissions = ['can_view_task']  # Specify the required permission for this view
    

class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]
    required_permissions = ['can_update_task']  # Specify the required permission for this view
    
class TaskDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]
    required_permissions = ['can_delete_task']  # Specify the required permission for this view