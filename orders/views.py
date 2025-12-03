import smtplib
from http import HTTPStatus
from importlib.metadata import metadata
from django.conf import settings
from django.core.mail import send_mail
import stripe
from django.urls.base import reverse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .forms import OrderForm
from django.conf import settings
from django.urls import reverse_lazy
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from .models import Order
from .models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

# Create your views here.

class SuccessTemplateView(TemplateView):
    template_name = 'orders/success.html'
    title = 'Успешно'
class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'

class OrderListView(ListView):
    template_name = 'orders/orders.html'
    title = 'Заказ'
    queryset = Order.objects.all()
    ordering = ['-created']
    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)

class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Детали #{self.object.id}'
        return context



class OrderCreateView(CreateView):
    template_name = "orders/order-create.html"
    form_class = OrderForm
    title = 'Neighbourhood - Заказы'
    success_url = reverse_lazy('orders:orders_create')

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.stripe_products(),
            metadata = {'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)
    def form_valid(self, form):
        form.instance.initiator = self.request.user
        response = super().form_valid(form)
        logger.info(f"Заказ создан пользователем {self.request.user}")
        return response
def fulfill_checkout(checkout_id):
    try:
        order = Order.objects.get(stripe_checkout_id=checkout_id)
        order.status = 'paid'
        order.save()
        try:
            send_mail(
                'Ваш заказ оплачен!',
                f'Номер заказа: {order.id}',
                settings.EMAIL_HOST_USER,
                [order.user.email],
                fail_silently=False,
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
            logger.info(f"Письмо отправлено на {order.user.email}")
        except smtplib.SMTPAuthenticationError:
            logger.error("Ошибка аутентификации SMTP")
        except smtplib.SMTPRecipientsRefused:
            logger.error("Адрес получателя отклонён")
        except Exception as e:
            logger.error(f"Неизвестная ошибка отправки: {e}")

    except Order.DoesNotExist:
        logger.warning(f"Заказ с checkout_id={checkout_id} не найден")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")




@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if ('data' in event and
            'object' in event['data'] and
            'id' in event['data']['object']):

        checkout_id = event['data']['object']['id']
        fulfill_checkout(checkout_id)  # Теперь функция существует!
    else:
        print("Неверные данные от Stripe:", event)
        return HttpResponseBadRequest("Invalid event data")

    return HttpResponse(status=200)
def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()


