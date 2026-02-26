from django.urls import path
from .views import MonthlySummaryView

urlpatterns = [
    path("monthly-summary/", MonthlySummaryView.as_view(), name="monthly-summary"),
]
