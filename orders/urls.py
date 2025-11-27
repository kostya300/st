from django.urls import path
from . import views
app_name = 'orders'
urlpatterns = [
    path('create/', OrdersCreateView.as_view(), name='orders_create'),

]