from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, VerificationCode


class InvitedUserInline(admin.TabularInline):
    model = User
    fk_name = "invited_by"
    extra = 0
    fields = ("phone_number", "invite_code", "is_active", "is_staff")
    readonly_fields = ("phone_number", "invite_code", "is_active", "is_staff")
    can_delete = False
    show_change_link = True


class UserAdmin(BaseUserAdmin):
    list_display = ("phone_number", "invite_code", "is_staff")
    search_fields = ("phone_number", "invite_code")
    ordering = ("phone_number",)
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            "Personal info",
            {"fields": ("invite_code", "activated_invite_code", "invited_by")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )
    inlines = [InvitedUserInline]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "password1", "password2"),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(VerificationCode)
