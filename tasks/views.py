from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView

from auth.jwt_auth import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer
from permissions.permissions import CanCreateTaskPermission, CanDeleteTaskPermission, CanUpdateTaskPermission, CanViewTaskPermission

class TaskCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanCreateTaskPermission]

class TaskListView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanViewTaskPermission]
    

class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanUpdateTaskPermission]
    
class TaskDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanDeleteTaskPermission]