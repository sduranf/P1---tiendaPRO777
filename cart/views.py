from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_products()
    quantities = cart.get_quantities()
    cart_total = cart.totals()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "cart_total": cart_total, "cart": cart.cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        final_image = request.POST.get('final_image')
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty, final_image=final_image)
        cart_quantity = cart.__len__()
        response = JsonResponse({'cart_quantity': cart_quantity})
        messages.success(request, f'¡Se ha agregado {product_qty} unidad(es) de "{product.name}" al carrito!')
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'cart_quantity': product_qty})
        return response