from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=1000)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
