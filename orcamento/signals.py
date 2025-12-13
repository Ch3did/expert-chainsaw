from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError

from orcamento.models.budget import BudgetProduct
from orcamento.models.product import Product


def _lock_product(product_id: int) -> Product:
    # trava a linha do produto pra evitar corrida de estoque
    return Product.objects.select_for_update().get(id=product_id)


@receiver(pre_save, sender=BudgetProduct)
def budgetproduct_pre_save(sender, instance: BudgetProduct, **kwargs):
    # guarda a quantidade antiga para calcular delta no post_save
    if instance.pk:
        old = BudgetProduct.objects.filter(pk=instance.pk).values("quantity").first()
        instance._old_quantity = old["quantity"] if old else 0
    else:
        instance._old_quantity = 0


@receiver(post_save, sender=BudgetProduct)
def budgetproduct_post_save(sender, instance: BudgetProduct, created: bool, **kwargs):
    # regra: só mexe no estoque antes de aprovação
    if instance.budget.is_approved:
        return

    new_qty = instance.quantity
    old_qty = getattr(instance, "_old_quantity", 0)
    delta = new_qty - old_qty

    if delta == 0:
        return

    with transaction.atomic():
        product = _lock_product(instance.product_id)

        # delta > 0 => precisa debitar mais do estoque
        if delta > 0:
            if product.stock_quantity < delta:
                raise ValidationError(
                    f"Estoque insuficiente para {product.name}. "
                    f"Disponível: {product.stock_quantity}, solicitado a mais: {delta}."
                )
            product.stock_quantity -= delta
            product.save(update_fields=["stock_quantity"])

        # delta < 0 => devolve estoque
        else:
            product.stock_quantity += (-delta)
            product.save(update_fields=["stock_quantity"])


@receiver(post_delete, sender=BudgetProduct)
def budgetproduct_post_delete(sender, instance: BudgetProduct, **kwargs):
    # ao deletar item do orçamento, devolve estoque (se não aprovado)
    if instance.budget.is_approved:
        return

    with transaction.atomic():
        product = _lock_product(instance.product_id)
        product.stock_quantity += instance.quantity
        product.save(update_fields=["stock_quantity"])
