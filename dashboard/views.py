from django.shortcuts import render

# Create your views here.

from django.db import models
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from transactions.models import Transaction, Category


class MonthlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.query_params.get("month")
        year = request.query_params.get("year")

        qs = Transaction.objects.filter(user=request.user)

        if year:
            qs = qs.filter(date__year=year)
        if month:
            qs = qs.filter(date__month=month)

        income = qs.filter(type="INCOME").aggregate(total=models.Sum("amount"))["total"] or 0
        expense = qs.filter(type="EXPENSE").aggregate(total=models.Sum("amount"))["total"] or 0

        # category-wise totals
        cat_totals = (
            qs.values("category__id", "category__name")
            .annotate(total=models.Sum("amount"))
            .order_by("-total")
        )

        return Response(
            {
                "total_income": income,
                "total_expense": expense,
                "savings": income - expense,
                "by_category": [
                    {
                        "category_id": c["category__id"],
                        "category_name": c["category__name"],
                        "total": c["total"],
                    }
                    for c in cat_totals
                ],
            }
        )
