from products.models import Basket


def baskets(request):
    if request.user.is_authenticated:
        user = request.user
        baskets = Basket.objects.filter(user=user)

        total_sum = sum(basket.sum() for basket in baskets)
        total_quantity = sum(basket.quantity for basket in baskets)

        context = {
            'baskets': baskets,
            'total_sum': total_sum,
            'total_quantity': total_quantity,
        }
    else:
        context = {
            'baskets': [],
            'total_sum': 0,
            'total_quantity': 0,
        }

    return  context


