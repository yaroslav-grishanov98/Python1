from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from payments.stripe_service import create_product, create_price, create_checkout_session
from materials.models import Course
from rest_framework import viewsets, permissions
from users.models import Payment
from users.serializers import PaymentSerializer




class StripeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Поле "name" обязательно'}, status=status.HTTP_400_BAD_REQUEST)
        description = request.data.get('description', '')
        try:
            product = create_product(name, description)
            return Response({'product_id': product.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripePriceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        unit_amount = request.data.get('unit_amount')
        if not product_id or not unit_amount:
            return Response({'error': 'Поля "product_id" и "unit_amount" обязательны'}, status=status.HTTP_400_BAD_REQUEST)
        currency = request.data.get('currency', 'usd')
        try:
            price = create_price(product_id, int(unit_amount), currency)
            return Response({'price_id': price.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        price_id = request.data.get('price_id')
        success_url = request.data.get('success_url')
        cancel_url = request.data.get('cancel_url')
        if not price_id or not success_url or not cancel_url:
            return Response({'error': 'Поля "price_id", "success_url" и "cancel_url" обязательны'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session = create_checkout_session(price_id, success_url, cancel_url)
            return Response({'checkout_url': session.url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        product = create_product(payment.paid_course.title, payment.paid_course.description)
        price = create_price(product.id, int(payment.amount * 100))
        session = create_checkout_session(
            price_id=price.id,
            success_url='https://your-site.com/success',
            cancel_url='https://your-site.com/cancel'
        )

        payment.stripe_session_url = session.url
        payment.save()
