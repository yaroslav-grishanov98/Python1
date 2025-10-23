from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from payments.stripe_service import create_product, create_price, create_checkout_session
from materials.models import Course

class StripeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description', '')
        product = create_product(name, description)
        return Response({'product_id': product.id})

class StripePriceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        unit_amount = request.data.get('unit_amount')
        currency = request.data.get('currency', 'usd')
        price = create_price(product_id, unit_amount, currency)
        return Response({'price_id': price.id})

class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        price_id = request.data.get('price_id')
        success_url = request.data.get('success_url')
        cancel_url = request.data.get('cancel_url')
        session = create_checkout_session(price_id, success_url, cancel_url)
        return Response({'checkout_url': session.url})
