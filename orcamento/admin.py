from django.contrib import admin
from .models import Service, Budget, BudgetService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "value")
    search_fields = ("name",)
    list_filter = ("value",)


class BudgetServiceInline(admin.TabularInline):
    model = BudgetService
    extra = 1
    autocomplete_fields = ("service",)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "bling_id", "value")
    search_fields = ("bling_id",)
    inlines = [BudgetServiceInline]
    readonly_fields = ("value",)

    def save_model(self, request, obj, form, change):
        # salva o Budget primeiro
        super().save_model(request, obj, form, change)
        # aqui ainda NÃO tem os inlines atualizados, então não recalcula aqui

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total_value()
