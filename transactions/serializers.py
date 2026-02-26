from rest_framework import serializers
from .models import Category, Transaction, RecurringTransaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "type", "is_default"]
        read_only_fields = ["id"]


class TransactionSerializer(serializers.ModelSerializer):
    # Read full category
    category = CategorySerializer(read_only=True)
    # Write by category id
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "type",
            "payment_mode",
            "date",
            "description",
            "category",
            "category_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class RecurringTransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = RecurringTransaction
        fields = [
            "id",
            "amount",
            "type",
            "frequency",
            "start_date",
            "end_date",
            "next_run_date",
            "is_active",
            "category",
            "category_id",
        ]
        read_only_fields = ["id"]
