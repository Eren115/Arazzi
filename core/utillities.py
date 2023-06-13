from .cart import Cart
from .models import Order, OrderItem

def checkout(request, email, full_name, street_address, city, state, zip, amount):
    order = Order.objects.create(full_name=full_name, email=email, street_address=street_address, city=city, state=state, zip=zip, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], price=item['product'].price, quantity=item['quantity'])

        # order.vendors.add(item['product'].vendor)

    return order