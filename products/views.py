from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import Product, ProductCategory, Basket
from users.models import User
# Create your views here.
def common(request):
    return render(request, "products/common.html")
def products(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products':Product.objects.all(),
    }
    return render(request, "products/products.html",context)


from django.shortcuts import redirect


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

