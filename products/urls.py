

from django.urls import path
from products.views import products, basket_add_product, basket_remove
app_name = 'products'
urlpatterns = [
    path('', products, name='catalog_general'),
    path('baskets/add/<int:product_id>/',basket_add_product, name='basket_add'),
    path('basket/remove/<int:basket_id>/',basket_remove, name='basket_remove'),
]
# 1234