from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import FileUploadLog, FactData

admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "date_joined", "is_staff")


@admin.register(FileUploadLog)
class FileUploadLogAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_email",
        "file_name",
        "upload_date",
        "status",
        "error_type",
    )

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = "E-mail користувача"


@admin.register(FactData)
class FactDataAdmin(admin.ModelAdmin):
    list_display = (
        "advertiser",
        "brand",
        "start_date",
        "end_date",
        "ad_format",
        "platform",
        "impressions",
    )
    list_filter = ("advertiser", "platform", "ad_format")
