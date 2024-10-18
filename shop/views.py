from django.shortcuts import render, redirect
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