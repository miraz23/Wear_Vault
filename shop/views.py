from django.shortcuts import render, redirect, get_object_or_404
from shop.models import product, order, orderUpdate
from math import ceil
from django.contrib import messages
import paypalrestsdk
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings

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
        messages.warning(request, "Login & Try Again")
        return redirect('/')
    
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')


        order_instance = order.objects.create(
            items_json=items_json,
            amount=amount,
            name=name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
        )
        request.session['order_id'] = order_instance.order_id


        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": f"http://localhost:8000/shop/payment/success/",
                "cancel_url": f"http://localhost:8000/shop/payment/cancel/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Your Product Name",
                        "sku": "Your Product SKU",
                        "price": amount,
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": amount,
                    "currency": "USD"},
                "description": "Order description."
            }]
        })

        if payment.create():
            print("Payment created successfully")
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    return redirect(approval_url)
                
            print("Payment ID:", payment.id)
            print("Order ID set in session:", request.session['order_id'])
        else:
            print(payment.error)

    return render(request, 'checkout.html')


def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    order_id = request.session.get('order_id')
    print("Order ID retrieved from session:", order_id)

    if not order_id:
        messages.error(request, "Order ID not found in session.")
        return redirect('shop')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        try:
            Order = get_object_or_404(order, order_id=order_id)
            Order.paymentstatus = "Paid"
            Order.oid = payment_id
            Order.amountpaid = Order.amount
            Order.save()

            update = orderUpdate(order_id=Order.order_id, update_desc="The order has been placed")
            update.save()

            # Send confirmation email to customer
            recipient_name = Order.name
            recipient_email = Order.email

            recipient_email_subject = "Order Confirmation"
            recipient_message = render_to_string('order-confirmation-email.html', {
                'customer_name': recipient_name,
                'order_id': Order.order_id,
                'amount': Order.amount,
                'payment_status': Order.paymentstatus,
                'domain': get_current_site(request).domain,
                'order_items': Order.formatted_items(),
            })

            recipient_email_message = EmailMessage(
                recipient_email_subject,
                recipient_message,
                settings.EMAIL_HOST_USER,
                [recipient_email]
            )

            recipient_email_message.content_subtype = "html"
            recipient_email_message.send()

            return render(request, 'payment_success.html')
        except Exception as e:
            print("Error fetching order:", e)
            messages.error(request, "There was an error processing your order.")
            return redirect('shop')
    else:
        messages.error(request, "Payment execution failed.")
        return render(request, 'payment_error.html')


def payment_cancel(request):
    return render(request, 'payment_cancel.html')

    
