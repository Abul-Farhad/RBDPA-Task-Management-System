from django.urls import path
from .views import AssignRolePermissionsView, CreateRoleView

urlpatterns = [
    path('assign/', AssignRolePermissionsView.as_view(), name="assign-permissions"),
    path('create-role/', CreateRoleView.as_view(), name="create-role"),
]
