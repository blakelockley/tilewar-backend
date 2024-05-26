from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.models import Token, TokenProxy
from django.contrib.auth.models import Group

from .forms import EmailUserChangeForm, EmailUserCreationForm
from .models import EmailUser


class AuthTokenInline(admin.TabularInline):
    model = Token
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj):
        return False


class EmailUserAdmin(UserAdmin):
    add_form = EmailUserCreationForm
    form = EmailUserChangeForm
    model = EmailUser

    ordering = (
        "is_staff",
        "-is_active",
        "-date_joined",
    )

    list_display = (
        "email",
        "is_active",
        "date_joined",
    )

    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )

    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("id", "email", "password", "is_active")}),
        (
            "Profile",
            {"fields": (("first_name", "last_name"), "avatar")},
        ),
        (
            "Auth",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "date_joined",
                    "auth_provider",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    (
                        "first_name",
                        "last_name",
                    ),
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    readonly_fields = ("id", "date_joined", "auth_provider")

    inlines = [AuthTokenInline]

    def logout_users(modeladmin, request, queryset):
        Token.objects.filter(user__in=queryset).delete()

    actions = [logout_users]


admin.site.register(EmailUser, EmailUserAdmin)

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
