from django.db import models



class Installment(models.Model):
    budget = models.ForeignKey(
        'orcamento.Budget',
        on_delete=models.CASCADE,
        related_name='installments'
    )
    number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()

    class Meta:
        ordering = ['number']

    @property
    def total_paid(self):
        return self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    @property
    def remaining(self):
        return self.amount - self.total_paid
