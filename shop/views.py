from django.shortcuts import render, redirect, get_object_or_404
from shop.models import product, order, orderUpdate
from math import ceil
from django.contrib import messages
import paypalrestsdk
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.conf import settings
from paypalrestsdk import Payment as PayPalPayment
import stripe

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
        # Common data
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = float(request.POST.get('amt'))  # Convert to float
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        payment_method = request.POST.get('payment_method', '')  # New field

        # Create an order instance
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

        if payment_method == 'paypal':
            # PayPal integration
            paypalrestsdk.configure({
                "mode": "sandbox",  # or "live"
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET
            })

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": request.build_absolute_uri('/shop/payment/success/'),
                    "cancel_url": request.build_absolute_uri('/shop/payment/cancel/')
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": f"Order #{order_instance.order_id}",
                            "sku": f"{order_instance.order_id}",
                            "price": amount,
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": "USD"
                    },
                    "description": f"Order #{order_instance.order_id}"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        return redirect(link.href)
            else:
                messages.error(request, f"PayPal error: {payment.error}")
                return redirect('/checkout/')

        elif payment_method == 'stripe':
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {'name': f"Order #{order_instance.order_id}"},
                            'unit_amount': int(amount * 100),
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/shop/payment/success/') + '?session_id={CHECKOUT_SESSION_ID}',
                    cancel_url=request.build_absolute_uri('/shop/payment/cancel/'),
                )
                return redirect(checkout_session.url, code=303)
            except Exception as e:
                messages.error(request, f"Stripe error: {e}")
                return redirect('/checkout/')

    return render(request, 'checkout.html')


def payment_success(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "Order ID not found in session.")
        return redirect('shop')

    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    stripe_session_id = request.GET.get('session_id')

    order_instance = get_object_or_404(order, order_id=order_id)

    if payment_id and payer_id:  # PayPal payment
        try:
            payment = PayPalPayment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                order_instance.paymentstatus = "Paid"
                order_instance.oid = payment_id
                order_instance.amountpaid = order_instance.amount
                order_instance.save()

                update = orderUpdate(order_id=order_instance.order_id, update_desc="The order has been placed")
                update.save()

                send_order_confirmation_email(order_instance)
                return render(request, 'payment_success.html')

        except Exception as e:
            print("Error processing PayPal payment:", e)
            messages.error(request, "An error occurred during payment processing.")
            return redirect('shop')

    elif stripe_session_id:  # Stripe payment
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            session = stripe.checkout.Session.retrieve(stripe_session_id)

            order_instance.oid = session.payment_intent
            order_instance.amountpaid = session.amount_total / 100
            order_instance.paymentstatus = "Paid"
            order_instance.save()

            update = orderUpdate(order_id=order_instance.order_id, update_desc="The order has been placed")
            update.save()

            send_order_confirmation_email(order_instance)
            return render(request, 'payment_success.html')

        except Exception as e:
            print("Error processing Stripe payment:", e)
            messages.error(request, "An error occurred during payment processing.")
            return redirect('shop')

    else:
        messages.error(request, "Payment details not found.")
        return redirect('shop')


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

    
