from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        # "is_superuser",
        "role",
    ]
    list_display = ["email", "username", "full_name", "role", "is_superuser"]

    def full_name(self, obj):
        return f"{obj.first_name}-{obj.last_name}"

    full_name.short_description = "Full Name"
