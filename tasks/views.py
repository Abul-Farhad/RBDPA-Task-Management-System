from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from django.db.models import Q

from auth.jwt_auth import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer
from permissions.permissions import HasRolePermission

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from .models import Task
from .serializers import TaskSerializer
from permissions.permissions import HasRolePermission
from auth.jwt_auth import JWTAuthentication
from accounts.models import CustomUser


class TaskCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def post(self, request):
        # Get data from the request
        serializer = TaskSerializer(data=request.data)

        # Validate and save the task
        if serializer.is_valid():
            task = serializer.save()

            return Response(
                {"message": "Task created successfully!", "data": TaskSerializer(task).data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def get(self, request):
        user = request.user
        task_id = request.data.get('task_id', None)  # Get task_id from query parameters
        

        if task_id:
            # If a task_id is provided, return that specific task
            try:
                task = Task.objects.get(id=task_id)

                # Ensure the user can view the task (either created by them or assigned to them, or if they are a superuser)
                if not user.is_superuser and not (task.created_by == user or task.assigned_to == user):
                    return Response({"error": "You do not have permission to view this task."}, status=status.HTTP_403_FORBIDDEN)

                # Serialize the task and return it
                serializer = TaskSerializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Task.DoesNotExist:
                raise NotFound(detail="Task not found")
        
        else:
            # If no task_id is provided, return the list of tasks for the user
            if user.is_superuser:
                tasks = Task.objects.all()
            else:
                tasks = Task.objects.filter(
                    Q(created_by=user) | Q(assigned_to=user)
                )

            # Serialize the tasks and return the list
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TaskUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def patch(self, request):
        # Retrieve task_id from request body
        task_id = request.data.get('task_id')
        user = request.user
        if not task_id:
            return Response({"error": "task_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the task based on ID
        task = Task.objects.filter(id=task_id).first()
        if not task:
            raise NotFound("Task not found.")
        if not user.is_superuser and not (task.created_by == user):
            return Response({"error": "You do not have permission to view this task."}, status=status.HTTP_403_FORBIDDEN)

        # Update the task with the request data
        serializer = TaskSerializer(task, data=request.data, partial=True)

        # Validate and save the updated task
        if serializer.is_valid():
            updated_task = serializer.save()

            return Response(
                {"message": "Task updated successfully!", "data": TaskSerializer(updated_task).data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def delete(self, request):
        task_id = request.data.get('task_id')
        user = request.user
        if not task_id:
            return Response({"error": "task_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the task based on ID
        task = Task.objects.filter(id=task_id).first()
        if not task:
            raise NotFound("Task not found.")
        if not user.is_superuser and not (task.created_by == user):
            return Response({"error": "You do not have permission to view this task."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the task
        task.delete()

        return Response({"message": "Task deleted successfully!"}, status=status.HTTP_200_OK)


class TaskAssignView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def post(self, request):
        task_id = request.data.get('task_id')
        user_id = request.data.get('user_id')
        user = request.user
        
        if not user.is_superuser and not (task.created_by == user):
            return Response({"error": "You do not have permission to view this task."}, status=status.HTTP_403_FORBIDDEN)
        if not task_id or not user_id:
            return Response({"error": "task_id and user_id are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the task based on ID
        task = Task.objects.filter(id=task_id).first()
        if not task:
            raise NotFound("Task not found.")

        # Assign the task to the user
        assigned_user = CustomUser.objects.filter(id=user_id).first()
        task.assigned_to = assigned_user
        task.save()

        return Response({"message": "Task assigned successfully!"}, status=status.HTTP_200_OK)
    
class TaskUnAssignView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [HasRolePermission]

    def post(self, request):
        task_id = request.data.get('task_id')
        user = request.user
        if not task_id:
            return Response({"error": "task_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the task based on ID
        task = Task.objects.filter(id=task_id).first()
        if not task:
            raise NotFound("Task not found.")
        if not user.is_superuser and not (task.created_by == user):
            return Response({"error": "You do not have permission to view this task."}, status=status.HTTP_403_FORBIDDEN)

        # Unassign the task from the user
        task.assigned_to = None
        task.save()

        return Response({"message": "Task unassigned successfully!"}, status=status.HTTP_200_OK)

# class TaskCreateView(CreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [HasRolePermission]

# class TaskListView(ListAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [HasRolePermission]
    

# class TaskUpdateView(UpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [HasRolePermission]
    
# class TaskDeleteView(DestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [HasRolePermission]