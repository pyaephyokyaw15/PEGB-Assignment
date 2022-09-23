from django.contrib import admin
from .models import Account, Department
from django.contrib.auth.admin import UserAdmin


# Create your models here.
class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active')}
         ),
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Departments', {
            'classes': ('wide',),
            'fields': ('department',)}
         ),
    )


class DepartmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


# Register models on admin site
admin.site.register(Account, AccountAdmin)
admin.site.register(Department, DepartmentAdmin)
