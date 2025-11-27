from locale import currency
from tkinter.font import names
from django.db import models
from users.models import User
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


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

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None, ):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(*args, force_insert=force_insert, force_update=force_update, using=using,
                                  update_fields=update_fields)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price * 100), currency='rub'
        )
        return stripe_product_price


#   new class basket
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

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