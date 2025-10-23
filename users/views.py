from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets, generics, filters, permissions, status
from .models import User, Payment, Subscription
from .serializers import UserSerializer, PaymentSerializer, RegisterSerializer
from .filters import PaymentFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from materials.models import Course
from drf_yasg.utils import swagger_auto_schema
from users.permissions import IsModerator
from drf_yasg import openapi


class UserListView(View):
    def get(self, request):
        return JsonResponse({'message': 'Список пользователей'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Получить список всех пользователей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создать нового пользователя")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Получить список всех платежей")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # убрали IsOwnerOr403

    @swagger_auto_schema(operation_description="Получить или обновить профиль текущего пользователя")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_description="Зарегистрировать нового пользователя")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Добавить или удалить подписку на курс",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['course_id'],
            properties={
                'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID курса')
            },
        ),
        responses={200: openapi.Response(description='Результат операции')}
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)
        subscription_qs = Subscription.objects.filter(user=user, course=course)

        if subscription_qs.exists():
            subscription_qs.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({'message': message})
