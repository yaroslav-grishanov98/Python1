from django.http import JsonResponse
from django.views import View
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer

class UserListView(View):
    def get(self, request):
        return JsonResponse({'message': 'Список пользователей'})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
