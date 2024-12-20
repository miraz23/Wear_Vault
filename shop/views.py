from django.shortcuts import render, redirect, get_object_or_404
from shop.models import product, order
from math import ceil
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import order

def shop(request, category=None):
    allProds = []

    if category:
        prod = product.objects.filter(product_category=category)
        if prod.exists():
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
        else:
            cat = category.replace("-", " ").title()
            return render(request, "shop.html", {
                'message': f"No products available in the '{cat}' category. Please check back later!"
            })
    else:
        catprods = product.objects.values('product_category', 'id')
        cats = {item['product_category'] for item in catprods}
        for cat in cats:
            prod = product.objects.filter(product_category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    
    data = {
        'allProds': allProds,
        'message': None if allProds else "No products available at the moment. Please check back later!"
    }
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
        messages.warning(request, "Login & Try Again")
        return redirect('/')
    

    context = {
        'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID,
    }
    return render(request, 'checkout.html', context)


@csrf_exempt
def payment_success(request):
    try:
        # Retrieve form data
        transaction_id = request.POST.get('transaction_id')
        items_json = request.POST.get('items_json')
        amount = request.POST.get('amount')  # From form
        amount_paid = request.POST.get('amount_paid')  # From PayPal
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        

        new_order = order(
            items_json=items_json,
            amount=amount,
            name=name,
            email=email,  # Save email
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            oid=transaction_id,
            amountpaid=amount_paid,  # Save amount paid
            paymentstatus="Success",
            phone=phone,
        )
        new_order.save()
        send_order_confirmation_email(new_order)

        return render(request, 'payment_success.html', {'order': new_order})
    
    except Exception as e:
        return render(request, 'payment_success.html', {'order': new_order})



def send_order_confirmation_email(order_instance):
    recipient_email_subject = "Order Confirmation"
    recipient_message = render_to_string('order-confirmation-email.html', {
        'customer_name': order_instance.name,
        'order_id': order_instance.order_id,
        'amount': order_instance.amount,
        'payment_status': order_instance.paymentstatus,
        'order_items': order_instance.formatted_items(),
    })

    recipient_email_message = EmailMessage(
        recipient_email_subject,
        recipient_message,
        settings.EMAIL_HOST_USER,
        [order_instance.email]
    )
    recipient_email_message.content_subtype = "html"
    recipient_email_message.send()


def payment_cancel(request):
    return render(request, 'payment_cancel.html')

    
