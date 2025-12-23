from django.db import models
from orcamento.models.installments import Installment
from django.core.exceptions import ValidationError

class Payment(models.Model):
    installment = models.ForeignKey(
        Installment,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    method = models.CharField(
        max_length=20,
        choices=[
            ('pix', 'Pix'),
            ('cash', 'Dinheiro'),
            ('card', 'Cartão'),
            ('transfer', 'Transferência'),
        ]
    )
    notes = models.TextField(blank=True)

    def clean(self):
        if self.installment and self.amount:
            if self.amount > self.installment.remaining:
                raise ValidationError(
                    {'amount': 'Valor do pagamento maior que o saldo da parcela.'}
                )