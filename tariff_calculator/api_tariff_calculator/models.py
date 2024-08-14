from django.db import models

class CalculationLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    tariff_unit = models.CharField(max_length=10)
    tariff_unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    started_at = models.DateTimeField()
    last_payment_time = models.DateTimeField(null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    unpaid_duration = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Log {self.timestamp} - Cost: {self.cost}"