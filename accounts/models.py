
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    SALARY_MONTHLY = "MONTHLY"
    SALARY_WEEKLY = "WEEKLY"
    SALARY_CUSTOM = "CUSTOM"

    SALARY_CYCLE_CHOICES = [
        (SALARY_MONTHLY, "Monthly"),
        (SALARY_WEEKLY, "Weekly"),
        (SALARY_CUSTOM, "Custom"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    default_currency = models.CharField(max_length=5, default="INR")
    salary_cycle = models.CharField(
        max_length=10,
        choices=SALARY_CYCLE_CHOICES,
        default=SALARY_MONTHLY,
    )
    timezone = models.CharField(max_length=50, default="Asia/Kolkata")

    def __str__(self):
        return f"Profile of {self.user.username}"
