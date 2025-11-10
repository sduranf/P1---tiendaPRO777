import datetime
from django.shortcuts import redirect, render, get_object_or_404
from cart.cart import Cart
from store.models import Profile, Product
from django.contrib import messages
from payment.forms import PaymentForm
from payment.models import Order, OrderItem
from django.contrib.auth.models import User

def order_details(request, order_id):
    # Conseguimos la orden o tiramos 404 si no existe
    order = get_object_or_404(Order, id=order_id)

    # Traemos los OrderItems asociados a esa orden
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'payment/order_details.html', context)

def not_shipped_orders(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)
            order.update(shipped=True, shipped_date=now)
            messages.success(request, f"La orden #{num} ha sido marcada como enviada.")
            return redirect('not_shipped_orders')
        return render(request, "payment/not_shipped_orders.html", {"orders": orders})
    else:
        messages.error(request, "No tienes permiso para ver esta página.")
        return redirect('home')

def shipped_orders(request):
    if request.user.is_authenticated and request.user.is_staff:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            num = request.POST['num']
            order = Order.objects.filter(id=num)
            order.update(shipped=False, shipped_date=None)
            messages.success(request, f"La orden #{num} ha sido marcada como no enviada.")
            return redirect('shipped_orders')
        return render(request, "payment/shipped_orders.html", {"orders": orders})
    else:
        messages.error(request, "No tienes permiso para ver esta página.")
        return redirect('home')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_products()
        quantities = cart.get_quantities()
        cart_total = cart.totals()
        payment_form = PaymentForm(request.POST or None)
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            shipping_info = {
                'full_name': profile.user.first_name + ' ' + profile.user.last_name,
                'email': profile.user.email,
                'phone': profile.phone,
                'address1': profile.address1,
                'address2': profile.address2,
                'city': profile.city,
                'state': profile.state,
                'zipcode': profile.zip_code,
                'country': profile.country,
            }

            
            full_name = shipping_info['full_name']
            email = shipping_info['email']
            shipping_address = f"{shipping_info['full_name']}\n{shipping_info['email']}\n{shipping_info['phone']}\n{shipping_info['address1']}\n{shipping_info['address2']}\n{shipping_info['city']}\n{shipping_info['state']}\n{shipping_info['zipcode']}\n{shipping_info['country']}"
            amount_paid = cart_total
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            order_id = create_order.pk
            
            for product in cart_products:
                product_id = str(product.id)
                cart_data = cart.cart.get(product_id)
                final_image = None
                if cart_data and len(cart_data) > 1:
                    final_image = cart_data[1]
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key,value in quantities.items():
                    if int(key) == product.id:
                        quantity = value
                create_order_item = OrderItem(
                    order_id=create_order.id,
                    product_id=product_id,
                    user=user,
                    quantity=quantity,
                    price=price,
                    final_image=final_image,
                )
                create_order_item.save()
            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
        else:
            messages.error(request, "Debes iniciar sesión para procesar la orden.")
            return redirect('home')

        messages.success(request, "¡Tu orden ha sido procesada con éxito!")
        return redirect('home')
        
    else:
        messages.error(request, "Acceso inválido al procesar la orden.")
        return redirect('home')

def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    cart_total = cart.totals()
    
    billing_form = PaymentForm()
    if request.user.is_authenticated:
        return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "cart_total": cart_total, "billing_form": billing_form})
    else:
        messages.error(request, "Debes iniciar sesión para ingresar la información de facturación.")
        return redirect('home')

def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    cart_total = cart.totals()
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "cart_total": cart_total, "profile": profile})
    else:
        messages.error(request, "Debes iniciar sesión para proceder al pago.")
        return redirect('home')
    
    
    
