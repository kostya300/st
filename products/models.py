from dis import RETURN_CONST
from locale import currency
from tkinter.font import names
from django.db import models
from users.models import User
from django.conf import settings
import logging
import stripe
from django.db import transaction
from django.core.exceptions import ValidationError
from decimal import ROUND_HALF_UP

stripe.api_key = settings.STRIPE_SECRET_KEY


from django.core.exceptions import ValidationError

class ProductCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='images/')
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.pk is None and not self.stripe_product_price_id:
            try:
                stripe_product_price = self.create_stripe_product_price()
                self.stripe_product_price_id = stripe_product_price['id']
            except stripe.error.StripeError as e:
                raise ValidationError(f"Ошибка в Stripe: {e}")
        super().save(force_insert, force_update, using, update_fields)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        unit_amount = int((self.price * 100).quantize(0, rounding=ROUND_HALF_UP))
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=unit_amount,
            currency=self.currency.lower(),
        )
        return stripe_product_price

    def update_stripe_price(self):
        if not self.stripe_product_price_id:
            return
        try:
            unit_amount = int((self.price * 100).quantize(0, rounding=ROUND_HALF_UP))
            stripe.Price.modify(
                self.stripe_product_price_id,
                unit_amount=unit_amount,
            )
        except stripe.error.StripeError as e:
            logger.error(f"Ошибка обновления цены в Stripe: {e}")


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.products_id.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'корзина для {self.user.email} | Продукт {self.products_id.name}'

    # cout price

    def sum(self):
        return self.products_id.price * self.quantity
    def de_json(self):
        basket_item = {
            'product': self.products_id.name,
            'quantity': self.quantity,
            'price': float(self.products_id.price),
            'sum': float(self.sum()),
        }
        return basket_item