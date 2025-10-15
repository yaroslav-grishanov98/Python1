from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from materials.models import Course, Lesson
from users.models import Payment
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Создать тестовые данные для пользователей, курсов, уроков и платежей'

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            email='testuser@example.com',
            defaults={'is_active': True, 'is_staff': False}
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Пользователь создан'))

        course, created = Course.objects.get_or_create(
            title='Тестовый курс',
            defaults={'description': 'Описание курса'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Курс создан'))

        lesson, created = Lesson.objects.get_or_create(
            course=course,
            title='Тестовый урок',
            defaults={'description': 'Описание урока', 'video_url': 'http://example.com/video'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Урок создан'))

        Payment.objects.create(
            user=user,
            paid_course=course,
            amount=1500,
            payment_method='cash',
            payment_date=timezone.now()
        )
        self.stdout.write(self.style.SUCCESS('Платеж за курс создан'))

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=500,
            payment_method='transfer',
            payment_date=timezone.now()
        )
        self.stdout.write(self.style.SUCCESS('Платеж за урок создан'))
