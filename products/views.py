from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.db.models import Sum
# Create your views here.
def common(request):
    return render(request, "products/common.html")
def products(request,category_id=None):
    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    context = {'categories':ProductCategory.objects.all(),'products':products,}
    return render(request, "products/products.html",context)


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





