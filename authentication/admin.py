from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'get_full_name', 'user_type', 'is_approved', 'institution', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_approved', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'institution', 'department')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth')}),
        ('User Type & Approval', {'fields': ('user_type', 'is_approved')}),
        ('Professional Info', {'fields': ('institution', 'department', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        ('User Type & Approval', {'fields': ('user_type', 'is_approved')}),
        ('Professional Info', {'fields': ('institution', 'department', 'bio')}),
    )
    
    actions = ['approve_instructors', 'disapprove_instructors']
    
    def approve_instructors(self, request, queryset):
        updated = queryset.filter(user_type='instructor').update(is_approved=True)
        self.message_user(request, f'{updated} instructor(s) approved successfully.')
    approve_instructors.short_description = "Approve selected instructors"
    
    def disapprove_instructors(self, request, queryset):
        updated = queryset.filter(user_type='instructor').update(is_approved=False)
        self.message_user(request, f'{updated} instructor(s) disapproved.')
    disapprove_instructors.short_description = "Disapprove selected instructors"

# Unregister the default Group admin if you don't need it
# admin.site.unregister(Group)
