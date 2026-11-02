from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.infrastructure.models import User, Follow


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("public_id", "bio", "avatar", "created_at", "updated_at")}),
    )
    readonly_fields = ("public_id", "created_at", "updated_at")


admin.site.register(Follow)
