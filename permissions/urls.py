from django.urls import path
from .views import AssignRoleView, AssignPermissionsView, CreateRoleView

urlpatterns = [
    path('assign-role/', AssignRoleView.as_view(), name="assign-permissions"),
    path('assign-permissions/', AssignPermissionsView.as_view(), name="assign-permissions"),
    path('create-role/', CreateRoleView.as_view(), name="create-role"),
]
