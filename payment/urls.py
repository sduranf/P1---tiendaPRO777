from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name='process_order'),
    path('shipped_orders/', views.shipped_orders, name='shipped_orders'),
    path('not_shipped_orders/', views.not_shipped_orders, name='not_shipped_orders'),
    path('orders/<int:order_id>/details/', views.order_details, name='order_details'),
]
