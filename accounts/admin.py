from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from .models import CustomUser
from permissions.models import UserRole, Role, Permission



# # Inline model for showing/editing role and permissions inside User admin page
# class UserRolesPermissionsInline(admin.StackedInline):
#     model = Role
#     can_delete = False
#     verbose_name_plural = 'Role & Permissions'
#     fk_name = 'user'

#     def get_max_num(self, request, obj=None, **kwargs):
#         # Limit to one role per user
#         return 1

#     def get_extra(self, request, obj=None, **kwargs):
#         # Prevent adding extra inline forms
#         return 0

#     def clean(self):
#         # Ensure only one role is assigned
#         if self.instance.userrolespermissions_set.count() > 1:
#             raise ValidationError("A user can only have one role.")


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = [
        'email', 
        'is_staff', 
        'is_active',
        'get_role',
        'get_permissions',
    ]
    search_fields = ['email']
#     inlines = [UserRolesPermissionsInline]  # 👈 Show role & permissions inside user admin form

    # === Custom display fields ===
    def get_role(self, obj):
        urp = UserRole.objects.filter(user=obj).first()
        return urp.role.name if urp else '—'
    get_role.short_description = 'Role'

    def get_permissions(self, obj):
        urp = UserRole.objects.filter(user=obj).first()
        return ', '.join(urp.role.permissions) if urp else '—'
    get_permissions.short_description = 'Permissions'
    # === Custom filters ===
    list_filter = (
        'is_staff',
        'is_active',
        ('user_roles__role', admin.RelatedOnlyFieldListFilter),
    )
    # === Custom search fields ===
    search_fields = ('email',)
    # === Custom ordering ===
    ordering = ('email',)

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
