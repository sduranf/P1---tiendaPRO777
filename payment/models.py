from django.db import models
from store.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    shipping_address = models.TextField(max_length=15000)
    amount_paid = models.IntegerField(default=0)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order - {str(self.id)}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)
    final_image = models.URLField(max_length=500, null=True, blank=True)


    def __str__(self):
        return f"{self.quantity} x {self.product.name} at {self.price} each"
