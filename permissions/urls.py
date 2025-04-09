from django.urls import path
from .views import AssignRoleView, CreateRoleView, UpdateRoleView, DeleteRoleView

urlpatterns = [
    path('assign-role/', AssignRoleView.as_view(), name="assign-role"),
    # path('assign-permissions/', AssignPermissionsView.as_view(), name="assign-permissions"),
    path('create-role/', CreateRoleView.as_view(), name="create-role"),
    path('update-role/', UpdateRoleView.as_view(), name="update-role"),
    path('delete-role/', DeleteRoleView.as_view(), name="delete-role"),
]
