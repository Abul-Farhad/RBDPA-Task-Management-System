from django.urls import path
from .views import TaskCreateView, TaskListView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name="create-task"),
    path('list/', TaskListView.as_view(), name="list-tasks"),
    path('update/<int:pk>/', TaskUpdateView.as_view(), name="update-task"),
    path('delete/<int:pk>/', TaskDeleteView.as_view(), name="delete-task"),
]
