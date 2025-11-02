from django.db import models
from users.models import User
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
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


#   new class basket
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.name

# pip install django-dump-load-utf8 for fixtures