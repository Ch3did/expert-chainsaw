from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, F, Sum
from django.db.models.functions import Coalesce

from orcamento.models.client import Client
from orcamento.models.product import Product
from orcamento.models.service import Service


class Budget(models.Model):
    bling_id = models.CharField(max_length=255, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_approved = models.BooleanField(default=False)
    services = models.ManyToManyField(
        Service,
        through="BudgetService",
        related_name="budgets",
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="budgets",
    )

    def __str__(self):
        return f"Budget #{self.id}"

    def update_total_value(self, commit=True):
        services_total = BudgetService.objects.filter(budget=self).aggregate(
            total=Coalesce(
                Sum(
                    F("unit_price") * F("quantity"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                Decimal("0.00"),
            )
        )["total"]

        products_total = BudgetProduct.objects.filter(budget=self).aggregate(
            total=Coalesce(
                Sum(
                    F("unit_price") * F("quantity"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                Decimal("0.00"),
            )
        )["total"]

        self.value = services_total + products_total

        if commit:
            self.save(update_fields=["value"])


class BudgetService(models.Model):
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="budget_services",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_budgets",
    )
    quantity = models.PositiveIntegerField(default=1)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("budget", "service")

    def save(self, *args, **kwargs):
        """
        Se o orçamento ainda não foi aprovado e o unit_price não foi definido,
        copia o valor atual do Service.
        """
        if self.unit_price is None and not self.budget.is_approved:
            self.unit_price = self.service.value
        super().save(*args, **kwargs)


class BudgetProduct(models.Model):
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        related_name="budget_product",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_budgets",
    )
    quantity = models.PositiveIntegerField(default=1)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("budget", "product")

    def save(self, *args, **kwargs):
        """
        Se o orçamento ainda não foi aprovado e o unit_price não foi definido,
        copia o valor atual do Product.
        """
        if self.unit_price is None and not self.budget.is_approved:
            self.unit_price = self.product.value
        super().save(*args, **kwargs)
