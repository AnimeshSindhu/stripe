import stripe
from .models import Product
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def send_prices_to_stripe():
    products = Product.objects.all()

    for product in products:
        price_cents = int(product.price * 100)

        stripe.Price.create(
            unit_amount=price_cents,
            currency='usd',
            product_data={
                'name': product.name
            }
        )
