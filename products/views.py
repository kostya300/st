from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView,CreateView
from unicodedata import category

from .models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# Create your views here.
class commonView(TemplateView):
    template_name = 'products/common.html'
    def get_context_data(self, **kwargs):
        context = super(commonView, self).get_context_data(**kwargs)
        context['title'] = 'Neighbourhood'


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 2
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Neighbourhood - List'
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add_product(request, product_id):
    if not request.user.is_authenticated:
        return redirect('users:login')

    product = Product.objects.get(id=product_id)

    try:
        # Ищем корзину с конкретным product_id
        basket = Basket.objects.get(user=request.user, products_id=product)
        basket.quantity += 1
        basket.save()
    except Basket.DoesNotExist:
        # Создаём новую запись, если корзины для этого продукта нет
        basket = Basket.objects.create(
            user=request.user,
            products_id=product,
            quantity=1
        )

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# basket_remove rm from basket controller for rm goods
@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.quantity -= 1
    basket.save()
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





