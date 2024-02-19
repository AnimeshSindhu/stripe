from django.shortcuts import redirect
from django.views import View
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import ListView
from .models import Product
from .stripe_utils import send_prices_to_stripe


class ProductLandingPageView(ListView):
    model = Product
    template_name = "landing.html"
    context_object_name = "book_list"


# Create your views here.
# class CreateCheckoutSessionView(View):
#     def post(self, request):
#         YOUR_DOMAIN = "http://127.0.0.1/8000"
#         send_prices_to_stripe()
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     # 'name': 'Book',
#                     'price': 'price_1Ok2A4SArpPtDUTg4Op5bw49',
#                     'quantity': 1,
#                 },
#             ],
#             mode='subscription',
#             success_url=YOUR_DOMAIN + '/success/',
#             cancel_url=YOUR_DOMAIN + '/cancel/',
#         )
#         return redirect(checkout_session.url, code=303)

# class CreatePaymentIntentView(View):
#     def post(self, request):
#         try:
#             stripe.api_key = settings.STRIPE_SECRET_KEY
#             intent = stripe.PaymentIntent.create(
#                 amount=2000,  # Amount in cents
#                 currency="usd",
#                 payment_method_configuration="pmc_1OlRi0SArpPtDUTgvNHOQlwZ",
#                 # payment_method_types=["card"],
#                 automatic_payment_methods={"enabled": True},
#             )
#             return JsonResponse({'intent': intent})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

class CreatePaymentIntentView(View):
    def post(self, request, *args, **kwargs):
        amount = request.POST.get('amount')
        payment_method_id = request.POST.get('payment_method_id')

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                payment_method=payment_method_id,
                confirm=True
            )

            return JsonResponse({'client_secret': payment_intent.client_secret})
        except stripe.error.CardError as e:
            # Handle card errors
            return JsonResponse({'error': str(e)}, status=400)
        except stripe.error.StripeError as e:
            # Handle other Stripe errors
            return JsonResponse({'error': str(e)}, status=400)


# class ConfirmPaymentIntentView(View):
#     def post(self, request):
#         try:
#             stripe.api_key = settings.STRIPE_SECRET_KEY
#             intent = stripe.PaymentIntent.confirm(
#                 payment_intent_id="pi_3OkLpqSArpPtDUTg0qkDScbS",
#                 payment_method="pm_card_visa",
#                 return_url="http://127.0.0.1:8000/",
#             )
#             return JsonResponse({'intent': intent})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
