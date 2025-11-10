from django.urls import path
from . import views

app_name = "customization"

urlpatterns = [
    path("personalizar/", views.personalizar, name="personalizar"),
    path("personalizar/<int:producto_id>/", views.personalizar, name="personalizar_producto"),
    path("generar-diseno-ia/", views.generar_diseno_ia, name="generar_diseno_ia"),
    path('product/<int:pk>/', views.product, name='product'),
]
