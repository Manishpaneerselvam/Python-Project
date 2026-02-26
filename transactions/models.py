# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    TYPE_INCOME = "INCOME"
    TYPE_EXPENSE = "EXPENSE"
    TYPE_BOTH = "BOTH"

    TYPE_CHOICES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
        (TYPE_BOTH, "Both"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="categories",
    )  # null/blank = global category if no user
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_EXPENSE)
    is_default = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "name", "type")

    def __str__(self):
        owner = self.user.username if self.user else "Global"
        return f"{self.name} ({self.type}) - {owner}"


class Transaction(models.Model):
    TYPE_INCOME = "INCOME"
    TYPE_EXPENSE = "EXPENSE"

    TYPE_CHOICES = [
        (TYPE_INCOME, "Income"),
        (TYPE_EXPENSE, "Expense"),
    ]

    PAYMENT_MODE_CASH = "CASH"
    PAYMENT_MODE_UPI = "UPI"
    PAYMENT_MODE_CARD = "CARD"
    PAYMENT_MODE_BANK = "BANK"
    PAYMENT_MODE_OTHER = "OTHER"

    PAYMENT_MODE_CHOICES = [
        (PAYMENT_MODE_CASH, "Cash"),
        (PAYMENT_MODE_UPI, "UPI"),
        (PAYMENT_MODE_CARD, "Card"),
        (PAYMENT_MODE_BANK, "Bank Transfer"),
        (PAYMENT_MODE_OTHER, "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        default=PAYMENT_MODE_OTHER,
    )
    date = models.DateField()
    description = models.TextField(blank=True)

    is_recurring_generated = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} {self.amount} on {self.date}"


class RecurringTransaction(models.Model):
    FREQUENCY_DAILY = "DAILY"
    FREQUENCY_WEEKLY = "WEEKLY"
    FREQUENCY_MONTHLY = "MONTHLY"
    FREQUENCY_YEARLY = "YEARLY"

    FREQUENCY_CHOICES = [
        (FREQUENCY_DAILY, "Daily"),
        (FREQUENCY_WEEKLY, "Weekly"),
        (FREQUENCY_MONTHLY, "Monthly"),
        (FREQUENCY_YEARLY, "Yearly"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recurring_transactions",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recurring_transactions",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(
        max_length=10,
        choices=Transaction.TYPE_CHOICES,
    )
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default=FREQUENCY_MONTHLY,
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    next_run_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.type} {self.amount} ({self.frequency})"
