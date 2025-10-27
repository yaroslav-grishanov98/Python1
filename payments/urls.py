from django.urls import path
from .views import StripeProductView, StripePriceView, StripeCheckoutSessionView

app_name = 'payments'

urlpatterns = [
    path('stripe/product/', StripeProductView.as_view(), name='stripe-product'),
    path('stripe/price/', StripePriceView.as_view(), name='stripe-price'),
    path('stripe/checkout-session/', StripeCheckoutSessionView.as_view(), name='stripe-checkout-session'),
]
