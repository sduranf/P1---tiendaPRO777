from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from items.models import Item, PurchaseReceipt


@login_required(login_url="login")
def add_to_cart(request, item_id):
    if "cart_items" in request.session.keys():
        # this if is for checking that items gets added only once
        if item_id not in request.session["cart_items"]:
            request.session["cart_items"].append(item_id)
    else:
        request.session["cart_items"] = [item_id]

    request.session.modified = True
    return redirect("cart:cart")


@login_required(login_url="login")
def remove_from_cart(request, item_id):
    request.session["cart_items"].remove(item_id)
    request.session.modified = True
    return redirect("cart:cart")


@login_required(login_url="login")
def cart(request):
    summ = 0
    if "cart_items" in request.session.keys():
        cart_items = []
        for cart_item_id in request.session["cart_items"]:
            item = Item.objects.get(pk=cart_item_id)
            cart_items.append(item)
            summ += item.discounted_price()
    else:
        cart_items = []

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "sum": summ,
        },
    )


@login_required(login_url="login")
def purchase(request):
    if len(request.session["cart_items"]) <= 0:
        return redirect("cart:cart")
    else:
        receipt = PurchaseReceipt(buyer=request.user)
        receipt.save()
        total = 0
        for item_id in request.session["cart_items"]:
            item = Item.objects.get(pk=item_id)
            receipt.items.add(item)
            total += item.discounted_price()
        receipt.total = total
        receipt.save()
        request.session.pop("cart_items")
        return redirect("user_profile:purchases")
