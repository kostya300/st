from django.contrib import admin
from django.contrib.auth.models import User
from .models import ProductCategory,Product

admin.site.register(ProductCategory)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','category')
    fields = ('image','name','description',('price','quantity'),'stripe_product_price_id','category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name',)

admin.site.register(Product)

