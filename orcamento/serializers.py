# serializers.py
from rest_framework import serializers

from .models.budget import Budget, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name", "value"]


class BudgetSerializer(serializers.ModelSerializer):
    # relação N:N via IDs de serviços
    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Service.objects.all(),
    )
    # valor calculado, apenas leitura
    value = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Budget
        fields = ["id", "services", "value", "bling_id"]

    def create(self, validated_data):
        services = validated_data.pop("services", [])
        budget = Budget.objects.create(**validated_data)
        budget.services.set(services)
        budget.update_total_value()
        return budget

    def update(self, instance, validated_data):
        services = validated_data.pop("services", None)

        # atualiza campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # se mandar services no payload, atualiza relação
        if services is not None:
            instance.services.set(services)

        instance.update_total_value()
        return instance
