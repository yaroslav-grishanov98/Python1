from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentListView, UserProfileView

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListView.as_view(), name='payment-list'),  # список платежей с фильтрацией
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # профиль текущего пользователя
]
