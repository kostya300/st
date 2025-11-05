from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from unicodedata import category

from .models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
# Create your views here.

class commonView(TemplateView):
    template_name = 'products/common.html'
    def get_context_data(self, **kwargs):
        context = super(commonView, self).get_context_data(**kwargs)
        context['title'] = 'Neighbourhood'
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Neighbourhood'
        context['categories'] = ProductCategory.objects.all()
        return context

# def products(request,category_id=None):
#     if category_id:
#         products_list = Product.objects.filter(category_id=category_id)
#     else:
#         products_list = Product.objects.all()
#     paginator = Paginator(products_list, 2)  # 2 товара на страницу
#     page_number = request.GET.get('page')  # Получаем номер страницы из запроса
#     page_obj = paginator.get_page(page_number)  # Получаем объект страницы
#     context = {'paginator': paginator,  # Передаём пагинатор для доступа к метаданным
#         'page_number': page_number,'categories':ProductCategory.objects.all(),'products':page_obj,}
#     return render(request, "products/products.html",context)


from django.shortcuts import redirect

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
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))





