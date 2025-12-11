from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Budget(models.Model):
    bling_id = models.CharField(max_length=255, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    services = models.ManyToManyField(
        Service,
        through="BudgetService",
        related_name="budgets",
    )

    def __str__(self):
        return f"Budget #{self.id}"

    def update_total_value(self):
        total = sum(
            bs.service.value * getattr(bs, "quantity", 1)
            for bs in self.budget_services.all()
        )
        self.value = total
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

    class Meta:
        unique_together = ("budget", "service")

    def __str__(self):
        return f"{self.budget} - {self.service}"
