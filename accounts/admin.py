
# Register your models here.
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "default_currency", "salary_cycle", "timezone")
    search_fields = ("user__username", "user__email")
