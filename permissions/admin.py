from django.contrib import admin
from permissions.models import Role, UserRole, Permission
# Register your models here.
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Permission)