from django.contrib import admin
from orcamento.models.service import Service
from orcamento.models.budget import Budget, BudgetService
from orcamento.models.client import Client


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "value")
    search_fields = ("name",)
    list_filter = ("value",)
    
    

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone")
    search_fields = ("name", "email")



class BudgetServiceInline(admin.TabularInline):
    model = BudgetService
    extra = 1
    autocomplete_fields = ("service",)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "bling_id", "value", "is_approved")
    search_fields = ("bling_id", "client",)
    list_filter = ("is_approved", "client",)
    inlines = [BudgetServiceInline]
    readonly_fields = ("value",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.update_total_value()
        
