from django.contrib import admin
from .models import Account, Department, CustomerCategory
from django.contrib.auth.admin import UserAdmin


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
        ('Customer Category', {
            'classes': ('wide',),
            'fields': ('customer_category',)}
         ),
    )

    # readonly_fields = ['customer_category']


# Register models on admin site
admin.site.register(Account, AccountAdmin)
admin.site.register(Department)
admin.site.register(CustomerCategory)
