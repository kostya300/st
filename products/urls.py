

from django.urls import path
from . import views
from .views import ProductListView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='catalog_general'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category_detail'),
    path('baskets/add/<int:product_id>/',views.basket_add_product, name='basket_add'),
    path('basket/remove/<int:basket_id>/',views.basket_remove, name='basket_remove'),

]
# 123