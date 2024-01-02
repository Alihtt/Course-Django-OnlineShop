from home.models import Product


CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        product_ids = cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart[str(product.id)]['product'] = product.name
        for item in cart.values():
            item['total_price'] = int(item['price']) * item['quantity']
            yield item

    def add(self, product, quantity):
        product_id = product.id
        if product not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True
