from django.shortcuts import render, redirect
from contact.models import contact
from shop.models import product

def index(request):
    drop_shoulders_count = product.objects.filter(product_category='drop-shoulders').count()
    baggy_joggers_count = product.objects.filter(product_category='baggy-joggers').count()
    baggy_shirts_count = product.objects.filter(product_category='baggy-shirts').count()
    cargo_pants_count = product.objects.filter(product_category='cargo-pants').count()
    head_wear_count = product.objects.filter(product_category='head-wear').count()
    baggy_shorts_count = product.objects.filter(product_category='baggy-shorts').count()

    latest_arrivals = product.objects.filter(latest_arrival='yes')

    data={
        'drop_shoulders_count' : drop_shoulders_count,
        'baggy_joggers_count' : baggy_joggers_count,
        'baggy_shirts_count' : baggy_shirts_count,
        'cargo_pants_count' : cargo_pants_count,
        'head_wear_count' : head_wear_count,
        'baggy_shorts_count' : baggy_shorts_count,
        'latest_arrivals': latest_arrivals,
    }

    return render(request, "index.html", data)

def aboutUs(request):
    return render(request, "about.html")

def contactUs(request):
    if request.method == 'POST':
       
        data = contact(
            contact_name = request.POST.get('contact-name'),
            contact_email = request.POST.get('contact-email'),
            contact_subject = request.POST.get('contact-subject'),
            contact_message = request.POST.get('contact-message'),
        )
        data.save()
        return redirect('/')
    
    return render(request, "contact.html")