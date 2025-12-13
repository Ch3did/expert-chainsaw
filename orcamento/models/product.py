from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Quantidade disponível em estoque",
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} (Estoque: {self.stock_quantity})"
