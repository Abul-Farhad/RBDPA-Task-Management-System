from django.urls import path
from .views import TaskAssignView, TaskCreateView, TaskListView, TaskUpdateView, TaskDeleteView, TaskUnAssignView

urlpatterns = [
    path('create-task/', TaskCreateView.as_view(), name="create-task"),
    path('list-tasks/', TaskListView.as_view(), name="list-tasks"),
    path('update-task/', TaskUpdateView.as_view(), name="update-task"),
    path('delete-task/', TaskDeleteView.as_view(), name="delete-task"),
    path('assign-task/', TaskAssignView.as_view(), name="assign-task"),
    path('unassign-task/', TaskUnAssignView.as_view(), name="unassign-task"),
]
