
# Register your models here.
from django.contrib import admin
from .models import Category, Transaction, RecurringTransaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "user", "is_default")
    list_filter = ("type", "is_default")
    search_fields = ("name", "user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "amount", "category", "payment_mode", "date")
    list_filter = ("type", "payment_mode", "date")
    search_fields = ("user__username", "description")
    date_hierarchy = "date"


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "amount", "frequency", "next_run_date", "is_active")
    list_filter = ("frequency", "is_active")
    search_fields = ("user__username",)
