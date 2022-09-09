from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User
from .forms import CustomUserChangeForm, CustomUserCreationForm


class CustomAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        "email",
        "username",
        "is_active",
        "is_superuser",
        "is_staff",
        "joined_date",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_superuser",
                ),
            },
        ),
    )
    list_filter = ("email", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Personal info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_superuser",)}),
    )


admin.site.register(User, CustomAdmin)
