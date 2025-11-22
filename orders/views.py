from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import OrderForm
from django.urls import reverse_lazy
import logging

logger = logging.getLogger(__name__)

# Create your views here.
class OrdersCreateView(CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    title = 'Neighbourhood - Заказы'
    success_url = reverse_lazy('orders:orders_create')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response = super().form_valid(form)
        logger.info(f"Заказ создан пользователем {self.request.user}")
        return response


