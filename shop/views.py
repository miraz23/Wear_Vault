from django.shortcuts import render, redirect, get_object_or_404
from shop.models import product, order, orderUpdate
from math import ceil
from django.contrib import messages

def shop(request, category=None):
    allProds = []
    
    if category:
        prod = product.objects.filter(product_category=category)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    else:
        catprods = product.objects.values('product_category', 'id')
        cats = {item['product_category'] for item in catprods}
        for cat in cats:
            prod = product.objects.filter(product_category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    
    data = {'allProds': allProds}
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

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login')

    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        Order = order(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = orderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True

    return render(request, 'checkout.html')
    
