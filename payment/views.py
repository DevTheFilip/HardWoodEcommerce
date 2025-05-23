from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.


from .models import ShippingAddress,Order,OrderItem

from cart.cart import Cart
from django.http import JsonResponse


def checkout(request):

    # Users with accounts --- pre-fill the form
    if request.user.is_authenticated:
        try:
            #authenticated user with shipping information
            shipping = ShippingAddress.objects.get(user=request.user.id)

            context = {'shipping': shipping}
            print("Authenticated user with shipping information")
            return render(request, 'payment/checkout.html',context=context)

        except ShippingAddress.DoesNotExist:
            return render(request, 'payment/checkout.html')


    return render(request, 'payment/checkout.html')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from .models import Order, OrderItem, Product

def payment_success(request):


    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]



    return render(request, 'payment/payment-succes.html')


def payment_failed(request):
    return render(request, 'payment/payment-failed.html')


def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        shipping_address = f"{address1}, {address2}, {city}, {state}, {zipcode}"

        cart = Cart(request)
        total_cost = cart.get_total()

        # Creează comanda
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost
            )

        items = []
        # Creează OrderItem
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['qty'],
                price=item['price'],
                user=request.user if request.user.is_authenticated else None
            )
            items.append({
                'product': item['product'],
                'quantity': item['qty'],
                'price': item['price'],
            })
            print(OrderItem)


        # Trimite email către admin
        current_site = get_current_site(request)
        subject = "HardWoodPellets - Comandă Nouă"
        html_message = render_to_string('payment/email.html', {
            'order': order,
            'items': items,
            'domain': current_site.domain
        })
        plain_message = strip_tags(html_message)


        print("Sending email to admin")
        send_mail(
            subject,
            plain_message,
            'hardwoodpellets1@gmail.com',
            ['szabo.andreeas@yahoo.com'],
            html_message=html_message,
        )
        print("Email sent to admin")

        return JsonResponse({'success': True})

    print("Failed to create order")
    return JsonResponse({'success': False})