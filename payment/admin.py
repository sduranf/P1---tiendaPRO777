from django.contrib import admin
from .models import Order, OrderItem
from django.contrib.auth.models import User

admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['date_ordered']
    inlines = [OrderItemInLine]
    
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)