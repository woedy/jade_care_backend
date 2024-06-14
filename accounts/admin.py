from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

from accounts.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('id', 'email', 'last_name', 'first_name', 'admin', 'is_doctor', 'is_patient',)
    list_filter = ('admin', 'staff', 'is_doctor', 'is_patient', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'last_name', 'first_name', 'password')}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active', 'is_doctor', 'is_patient',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )

    search_fields = ('email', 'last_name', 'first_name',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)