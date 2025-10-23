from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PaymentListView, UserProfileView, RegisterView, SubscriptionView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]
