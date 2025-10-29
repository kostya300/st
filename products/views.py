from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, ProductCategory


# Create your views here.
def common(request):
    return render(request, "products/common.html")
def products(request):
    context = {
        'categories': ProductCategory.objects.all(),
        'products':Product.objects.all(),
    }
    return render(request, "products/products.html",context)