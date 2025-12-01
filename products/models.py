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

    def save(self, *args, **kwargs):
        if self.pk:  # Если объект уже существует
            old_price = Product.objects.get(pk=self.pk).price
            if self.price != old_price:
                # Цена изменилась — создаём новую цену в Stripe
                stripe_product_price = self.create_stripe_product_price()
                self.stripe_product_price_id = stripe_product_price['id']
        elif not self.stripe_product_price_id:  # Новый объект
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super().save(*args, **kwargs)

    def create_stripe_product_price(self):
        try:
            stripe_product = stripe.Product.create(name=self.name)
            stripe_product_price = stripe.Price.create(
                product=stripe_product['id'],
                unit_amount=round(self.price * 100),
                currency='rub'
            )
            return stripe_product_price
        except stripe.error.StripeError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Ошибка Stripe: {e}")
            raise


# 123
    def sync_stripe_price(self):
        """Синхронизирует цену в Stripe с локальной"""
        if not self.stripe_product_price_id:
            return self.create_stripe_product_price()

        current_price = round(self.price * 100)
        stripe_price = stripe.Price.retrieve(self.stripe_product_price_id)

        if stripe_price.unit_amount != current_price:
            new_price = stripe.Price.create(
                product=stripe_price.product,
                unit_amount=current_price,
                currency='rub'
            )
            self.stripe_product_price_id = new_price.id
            self.save()
# 123

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
<<<<<<< HEAD
            'product': self.products_id.name,
            'quantity': self.quantity,
            'price': float(self.products_id.price),
            'sum': float(self.sum()),
        }
=======
            'product_id': self.products_id.id if self.products_id else None,
            'product_name': self.products_id.name if self.products_id else 'Неизвестно',
            'quantity': self.quantity,
            'sum': float(self.sum()) if self.sum() is not None else 0.0,
        }

>>>>>>> mainst
        return basket_item