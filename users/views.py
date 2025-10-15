from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, generics, filters
from .models import User, Payment
from .serializers import UserSerializer, PaymentSerializer
from .filters import PaymentFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class UserListView(View):
    def get(self, request):
        return JsonResponse({'message': 'Список пользователей'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
