from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User

@shared_task
def deactivate_inactive_users():
    threshold_date = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(last_login__lt=threshold_date, is_active=True)
    users_to_deactivate.update(is_active=False)