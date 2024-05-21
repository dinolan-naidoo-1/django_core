from django.db import models
import uuid

class TransactionData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    country = models.CharField(max_length=2)  # ISO 3166 code
    transaction_type = models.CharField(max_length=10)  # 'purchase' or 'sale'
    currency = models.CharField(max_length=3)  # ISO 4217 code
    net_amount = models.DecimalField(max_digits=20, decimal_places=2)
    input_amount = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Transaction data'

    def __str__(self):
        return f"{self.date} - {self.country} - {self.currency} - {self.transaction_type}"