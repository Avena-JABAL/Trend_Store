class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, roupa_id, quantity=1):
        roupa_id = str(roupa_id)
        if roupa_id not in self.cart:
            self.cart[roupa_id] = {'quantity': 0}
        
        self.cart[roupa_id]['quantity'] += quantity
        self.save()

    def remove(self, roupa_id):
        roupa_id = str(roupa_id)
        if roupa_id in self.cart:
            del self.cart[roupa_id]
            self.save()
    
    def save(self):
        self.session.modified = True
        