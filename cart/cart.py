from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart
    
    def add(self, product, quantity, final_image):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id in self.cart:
            self.cart[product_id] = (self.cart[product_id][0] + int(product_qty), final_image)
        else:
            self.cart[product_id] = (int(product_qty), final_image)
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantities(self):
        quantities = {}
        for key, value in self.cart.items():
            quantities[key] = value[0]
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        if product_id in self.cart:
            self.cart[product_id] = product_qty
        self.session.modified = True
        return self.cart
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
        
    def totals(self):
        total = 0
        for product_id, (quantity, image) in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                price = product.sale_price if product.is_sale else product.price
                subtotal = price * quantity
                total += subtotal
            except Product.DoesNotExist:
                continue
        return total