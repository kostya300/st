from django.contrib import admin
from django.contrib.auth.models import User
from .models import ProductCategory,Product

admin.site.register(ProductCategory)
admin.site.register(Product)