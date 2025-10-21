from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from materials.models import Course, Lesson
from users.models import Subscription
from django.core.files.uploadedfile import SimpleUploadedFile


class LessonSubscriptionTests(APITestCase):
    def setUp(self):
        self.moderator = User.objects.create_user(email='mod@example.com', password='password123')
        self.moderator.groups.create(name='moderators')
        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')

        self.course = Course.objects.create(title='Test Course', description='Desc', owner=self.user1, preview='')

        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Desc',
            preview='',
            video_url='https://youtube.com/watch?v=abc',
            owner=self.user1
        )

    def get_token(self, user):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('materials:lesson-list-create')

        # Минимальное валидное изображение PNG
        image_content = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00'
            b'\x00\x00\nIDATx\xdac\xfc\xff\xff?\x00\x05\xfe\x02\xfeA'
            b'\x0b\xcb\x81\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        image = SimpleUploadedFile("test.png", image_content, content_type="image/png")

        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'New Desc',
            'preview': image,
            'video_url': 'https://youtube.com/watch?v=xyz'
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('materials:lesson-list-create')
        data = {
            'course': self.course.id,
            'title': 'Mod Lesson',
            'description': 'Desc',
            'video_url': 'https://youtube.com/watch?v=xyz'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('materials:lesson-detail', kwargs={'pk': self.lesson.id})
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Lesson')

    def test_update_lesson_non_owner_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('materials:lesson-detail', kwargs={'pk': self.lesson.id})
        data = {'title': 'Hacked Lesson'}
        response = self.client.patch(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_update_lesson_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('materials:lesson-detail', kwargs={'pk': self.lesson.id})
        data = {'title': 'Moderator Updated'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('materials:lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_non_owner_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('materials:lesson-detail', kwargs={'pk': self.lesson.id})
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_subscription_add_and_remove(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('users:subscription')
        data = {'course_id': self.course.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Подписка добавлена', response.data['message'])

        self.assertTrue(Subscription.objects.filter(user=self.user1, course=self.course).exists())

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Подписка удалена', response.data['message'])

        self.assertFalse(Subscription.objects.filter(user=self.user1, course=self.course).exists())
