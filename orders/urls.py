from django.urls import path
from . import views
from .views import OrderCreateView,SuccessTemplateView,CanceledTemplateView
app_name = 'orders'
urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='orders_create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),

]