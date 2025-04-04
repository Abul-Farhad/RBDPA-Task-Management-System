from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import CustomUser
from permissions.models import UserRolesPermissions


# Inline model for showing/editing role and permissions inside User admin page
class UserRolesPermissionsInline(admin.StackedInline):
    model = UserRolesPermissions
    can_delete = False
    verbose_name_plural = 'User Role & Permissions'
    fk_name = 'user'

    def get_max_num(self, request, obj=None, **kwargs):
        # Limit to one role per user
        return 1

    def get_extra(self, request, obj=None, **kwargs):
        # Prevent adding extra inline forms
        return 0

    def clean(self):
        # Ensure only one role is assigned
        if self.instance.userrolespermissions_set.count() > 1:
            raise ValidationError("A user can only have one role.")


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = [
        'email', 
        'is_staff', 
        'is_active',
        'get_role',
        'can_create_task',
        'can_view_task',
        'can_update_task',
        'can_delete_task',
        'can_assign_team'
    ]
    search_fields = ['email']
    inlines = [UserRolesPermissionsInline]  # 👈 Show role & permissions inside user admin form

    # === Custom display fields ===
    def get_role(self, obj):
        urp = UserRolesPermissions.objects.filter(user=obj).first()
        return urp.role.name if urp else '—'
    get_role.short_description = 'Role'

    def can_create_task(self, obj):
        urp = UserRolesPermissions.objects.filter(user=obj).first()
        return urp.can_create_task if urp else False
    can_create_task.boolean = True
    can_create_task.short_description = 'Create'
    
    def can_view_task(self, obj):
        urp = UserRolesPermissions.objects.filter(user=obj).first()
        return urp.can_view_task if urp else False
    can_view_task.boolean = True
    can_view_task.short_description = 'View'

    def can_update_task(self, obj):
        urp = UserRolesPermissions.objects.filter(user=obj).first()
        return urp.can_update_task if urp else False
    can_update_task.boolean = True
    can_update_task.short_description = 'Update'

    def can_delete_task(self, obj):
        urp = UserRolesPermissions.objects.filter(user=obj).first()
        return urp.can_delete_task if urp else False
    can_delete_task.boolean = True
    can_delete_task.short_description = 'Delete'

    def can_assign_team(self, obj):
        urp = UserRolesPermissions.objects.filter(user=obj).first()
        return urp.can_assign_team if urp else False
    can_assign_team.boolean = True
    can_assign_team.short_description = 'Assign Team'

    # === Field layout in the admin form ===
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
