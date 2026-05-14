from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from .models import User, PreRegisteredUser, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display    = ('email', 'full_name', 'role', 'assistant_type', 'department', 'is_active', 'date_joined')
    list_filter     = ('role', 'is_active', 'is_staff')
    search_fields   = ('email', 'full_name', 'department')
    ordering        = ('email',)

    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal',     {'fields': ('full_name', 'role', 'department')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates',        {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'full_name', 'role', 'department', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')

    @admin.display(description='Assistant Type')
    def assistant_type(self, obj):
        if obj.role != 'assistant':
            return '—'
        return 'Main Assistant' if obj.is_main_assistant else f'Dept Assistant ({obj.department})'

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)


@admin.register(PreRegisteredUser)
class PreRegisteredUserAdmin(admin.ModelAdmin):
    list_display   = ('email', 'role', 'department', 'status_badge', 'created_at')
    list_filter    = ('role', 'registered')
    search_fields  = ('email', 'department')
    ordering       = ('role', 'email')
    readonly_fields = ('created_at', 'registered')

    fieldsets = (
        ('User Details', {
            'fields': ('email', 'role', 'department'),
            'description': (
                'Add the email and role of a user so they can self-register. '
                'The department field is required for Faculty/Student and Dept-Assistant, '
                'and should be left blank for the Main (Super) Assistant.'
            ),
        }),
        ('Status', {
            'fields': ('registered', 'created_at'),
        }),
    )

    @admin.display(description='Registration Status')
    def status_badge(self, obj):
        if obj.registered:
            return format_html(
                '<span style="background:#e8f5e9;color:#2e7d32;padding:2px 10px;'
                'border-radius:20px;font-size:.78rem;font-weight:700;">✓ Registered</span>'
            )
        return format_html(
            '<span style="background:#fff8e1;color:#e65100;padding:2px 10px;'
            'border-radius:20px;font-size:.78rem;font-weight:700;">⏳ Pending</span>'
        )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display  = ('user', 'token', 'created_at', 'used', 'valid_status')
    list_filter   = ('used',)
    search_fields = ('user__email',)
    readonly_fields = ('token', 'created_at')

    @admin.display(description='Valid?', boolean=True)
    def valid_status(self, obj):
        return obj.is_valid()
