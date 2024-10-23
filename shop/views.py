from django.shortcuts import render, redirect, get_object_or_404
from shop.models import product
from math import ceil

def shop(request):

    allProds = []
    catprods = product.objects.values('product_category','id')
    print(catprods)
    cats = {item['product_category'] for item in catprods}
    for cat in cats:
        prod= product.objects.filter(product_category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    data = {'allProds':allProds}

    return render(request, "shop.html", data)

def productDetails(request, id):
    prod = get_object_or_404(product, id=id)
    colors = prod.product_color.split(",")
    sizes = prod.product_size.split(",")

    data = {
        'product': prod,
        'colors': colors,
        'sizes': sizes,
    }
    return render(request, "quickview.html", data)
