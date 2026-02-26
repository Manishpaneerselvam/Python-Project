from datetime import timedelta, date

from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Transaction, RecurringTransaction
from .serializers import (
    CategorySerializer,
    TransactionSerializer,
    RecurringTransactionSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # global categories (user is null) + user-specific
        return Category.objects.filter(
            models.Q(user__isnull=True) | models.Q(user=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user).order_by("-date")

        # optional filters
        tx_type = self.request.query_params.get("type")
        category_id = self.request.query_params.get("category")
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if tx_type in ["INCOME", "EXPENSE"]:
            qs = qs.filter(type=tx_type)

        if category_id:
            qs = qs.filter(category_id=category_id)

        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)

        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        qs = self.get_queryset()
        income = qs.filter(type="INCOME").aggregate(total=models.Sum("amount"))["total"] or 0
        expense = qs.filter(type="EXPENSE").aggregate(total=models.Sum("amount"))["total"] or 0
        return Response(
            {
                "total_income": income,
                "total_expense": expense,
                "savings": income - expense,
            }
        )


class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RecurringTransaction.objects.filter(
            user=self.request.user
        ).order_by("next_run_date")

    def perform_create(self, serializer):
        # if next_run_date not sent, default to start_date
        instance = serializer.save(user=self.request.user)
        if not instance.next_run_date:
            instance.next_run_date = instance.start_date
            instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.next_run_date:
            instance.next_run_date = instance.start_date
            instance.save()

    def _increment_next_run_date(self, obj: RecurringTransaction):
        """Move next_run_date forward based on frequency."""
        current = obj.next_run_date
        if obj.frequency == RecurringTransaction.FREQUENCY_DAILY:
            obj.next_run_date = current + timedelta(days=1)
        elif obj.frequency == RecurringTransaction.FREQUENCY_WEEKLY:
            obj.next_run_date = current + timedelta(weeks=1)
        elif obj.frequency == RecurringTransaction.FREQUENCY_MONTHLY:
            # simple month increment (safe version)
            month = current.month + 1
            year = current.year
            if month > 12:
                month = 1
                year += 1
            # keep day <= 28 to avoid invalid dates
            day = min(current.day, 28)
            obj.next_run_date = current.replace(year=year, month=month, day=day)
        elif obj.frequency == RecurringTransaction.FREQUENCY_YEARLY:
            year = current.year + 1
            day = min(current.day, 28)
            obj.next_run_date = current.replace(year=year, day=day)

    @action(detail=False, methods=["post"])
    def run_due(self, request):
        """Generate real transactions for all due recurring rules."""
        today = date.today()

        qs = self.get_queryset().filter(
            is_active=True,
            next_run_date__lte=today,
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=today)
        )

        created_count = 0

        for rt in qs:
            # create a Transaction for this occurrence
            Transaction.objects.create(
                user=request.user,
                category=rt.category,
                amount=rt.amount,
                type=rt.type,
                payment_mode=Transaction.PAYMENT_MODE_OTHER,
                date=rt.next_run_date,
                description=f"Recurring: {rt.category.name if rt.category else ''}",
                is_recurring_generated=True,
            )
            created_count += 1

            # move next_run_date forward
            self._increment_next_run_date(rt)
            rt.save()

        return Response(
            {"detail": f"{created_count} transactions created."}
        )
