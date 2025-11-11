import datetime
from django.shortcuts import redirect, render, get_object_or_404
from cart.cart import Cart
from store.models import Profile, Product
from django.contrib import messages
from payment.forms import PaymentForm
from payment.models import Order, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

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

@login_required
def order_history(request):
    """Vista para mostrar el historial de compras del usuario"""
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    # Agrupar órdenes por mes para mejor organización
    orders_by_month = {}
    for order in orders:
        month_key = order.date_ordered.strftime('%Y-%m')
        if month_key not in orders_by_month:
            orders_by_month[month_key] = []
        orders_by_month[month_key].append(order)
    
    context = {
        'orders': orders,
        'orders_by_month': orders_by_month,
    }
    
    return render(request, 'payment/order_history.html', context)

@login_required
def generate_receipt(request, order_id):
    """Genera un recibo en PDF para una orden específica"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    # Crear el buffer para el PDF
    buffer = BytesIO()
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    
    # Contenedor para los elementos del PDF
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#198754'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0f5132'),
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )
    
    # Título
    title = Paragraph("KulturaUrbana", title_style)
    elements.append(title)
    
    subtitle = Paragraph("Recibo de Compra", styles['Heading2'])
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    
    # Información de la empresa
    company_info = [
        ["<b>KulturaUrbana</b>", ""],
        ["Tienda de Camisas Personalizadas", ""],
        ["Email: info@kulturaurbana.com", f"<b>Orden #:</b> {order.id}"],
        ["Teléfono: +1 (555) 123-4567", f"<b>Fecha:</b> {order.date_ordered.strftime('%d/%m/%Y %H:%M')}"],
    ]
    
    company_table = Table(company_info, colWidths=[4*inch, 2.5*inch])
    company_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(company_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Línea divisoria
    elements.append(Spacer(1, 0.1*inch))
    
    # Información del cliente
    client_heading = Paragraph("<b>Información del Cliente</b>", heading_style)
    elements.append(client_heading)
    
    # Parsear dirección de envío
    shipping_lines = order.shipping_address.split('\n')
    client_info_text = f"""
    <b>Nombre:</b> {order.full_name}<br/>
    <b>Email:</b> {order.email}<br/>
    <b>Dirección de envío:</b><br/>
    """
    for line in shipping_lines:
        if line.strip():
            client_info_text += f"&nbsp;&nbsp;&nbsp;&nbsp;{line.strip()}<br/>"
    
    client_info = Paragraph(client_info_text, normal_style)
    elements.append(client_info)
    elements.append(Spacer(1, 0.2*inch))
    
    # Estado de la orden
    status_text = "Enviada" if order.shipped else "Pendiente"
    status_color = colors.HexColor('#198754') if order.shipped else colors.HexColor('#ffc107')
    status_style = ParagraphStyle(
        'StatusStyle',
        parent=normal_style,
        textColor=status_color,
        fontName='Helvetica-Bold'
    )
    status = Paragraph(f"<b>Estado:</b> {status_text}", status_style)
    elements.append(status)
    elements.append(Spacer(1, 0.2*inch))
    
    # Productos
    products_heading = Paragraph("<b>Productos</b>", heading_style)
    elements.append(products_heading)
    
    # Tabla de productos
    product_data = [['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal']]
    
    total = 0
    for item in order_items:
        product_name = item.product.name if item.product else "Producto eliminado"
        quantity = item.quantity
        price = item.price
        subtotal = quantity * price
        total += subtotal
        
        product_data.append([
            product_name,
            str(quantity),
            f"${price:,}",
            f"${subtotal:,}"
        ])
    
    # Agregar fila de total
    product_data.append(['', '', '<b>TOTAL</b>', f'<b>${total:,}</b>'])
    
    product_table = Table(product_data, colWidths=[3*inch, 1*inch, 1.2*inch, 1.2*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#198754')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTSIZE', (0, 1), (-1, -2), 10),
        ('FONTSIZE', (0, -1), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -2), 8),
        ('TOPPADDING', (0, 1), (-1, -2), 8),
        ('GRID', (0, 0), (-1, -2), 1, colors.grey),
        ('GRID', (0, -1), (-1, -1), 2, colors.HexColor('#198754')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d1e7dd')),
    ]))
    elements.append(product_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Notas
    notes_heading = Paragraph("<b>Notas</b>", heading_style)
    elements.append(notes_heading)
    
    notes_text = """
    Gracias por tu compra en KulturaUrbana. Si tienes alguna pregunta sobre tu pedido, 
    por favor contáctanos a través de nuestro email o teléfono.
    <br/><br/>
    <i>Este es un recibo generado automáticamente. Por favor, guárdalo para tus registros.</i>
    """
    notes = Paragraph(notes_text, normal_style)
    elements.append(notes)
    
    # Construir el PDF
    doc.build(elements)
    
    # Obtener el valor del buffer y crear la respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recibo_orden_{order.id}.pdf"'
    
    return response