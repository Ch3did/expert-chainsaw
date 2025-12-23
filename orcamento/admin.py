from django.contrib import admin

from orcamento.models.budget import Budget, BudgetService, BudgetProduct
from orcamento.models.client import Client
from orcamento.models.product import Product
from orcamento.models.service import Service
from orcamento.models.payments import Payment
from orcamento.models.installments import Installment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "installment", "amount", "payment_date", "method")
    search_fields = ("installment__budget__bling_id", "installment__number")
    list_filter = ("method", "payment_date")
    
class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ("id", "budget", "number", "amount", "remaining")
    inlines = [PaymentInline]
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "value")
    search_fields = ("name",)
    list_filter = ("value",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "unit_price",
        "stock_quantity"
    )
    search_fields = (
        "name",
        "stock_quantity"
    )


class BudgetServiceInline(admin.TabularInline):
    model = BudgetService
    extra = 1
    autocomplete_fields = ("service",)


class BudgetProductInline(admin.TabularInline):
    model = BudgetProduct
    extra = 1
    autocomplete_fields = ("product",)



@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "bling_id", "value", "is_approved")
    search_fields = (
        "bling_id",
        "client",
    )
    list_filter = (
        "is_approved",
        "client",
    )
    inlines = [BudgetServiceInline, BudgetProductInline]
    readonly_fields = ("value",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total_value()
