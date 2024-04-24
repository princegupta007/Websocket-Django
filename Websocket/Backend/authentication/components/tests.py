from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
from account.models import CustomUser  # Update this with the correct import path
from .views import DashboardView

class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create a superadmin user
        self.superadmin = CustomUser.objects.create_user(username='superadmin', user_type='superadmin')
        self.superadmin_access_token = AccessToken.for_user(self.superadmin)

        # Create an admin user
        self.admin = CustomUser.objects.create_user(username='admin', user_type='admin', parent_admin=self.superadmin)
        self.admin_access_token = AccessToken.for_user(self.admin)

        # Create a teacher user
        self.teacher = CustomUser.objects.create_user(username='teacher', user_type='teacher', parent_admin=self.admin)
        self.teacher_access_token = AccessToken.for_user(self.teacher)

        # Create a student user
        self.student1 = CustomUser.objects.create_user(username='student1', user_type='student', parent_admin=self.admin)
        self.student2 = CustomUser.objects.create_user(username='student2', user_type='student', parent_admin=self.admin)
        self.student_access_token = AccessToken.for_user(self.student1)

    def test_superadmin_dashboard(self):
        request = self.factory.get('/dashboard/', HTTP_AUTHORIZATION=f'Bearer {self.superadmin_access_token}')
        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['admin_count'], 1)  # Assuming only one admin in the database
        self.assertEqual(response.data['teacher_count'], 1)  # Assuming only one teacher in the database
        self.assertEqual(response.data['student_count'], 2)  # Assuming two students in the database

    def test_admin_dashboard(self):
        request = self.factory.get('/dashboard/', HTTP_AUTHORIZATION=f'Bearer {self.admin_access_token}')
        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['teacher_count'], 1)  # Assuming only one teacher in the database
        self.assertEqual(response.data['student_count'], 2)  # Assuming two students in the database

    def test_teacher_dashboard(self):
        request = self.factory.get('/dashboard/', HTTP_AUTHORIZATION=f'Bearer {self.teacher_access_token}')
        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['student_count'], 0)  # Assuming no students for the teacher in the database


    def test_student_dashboard(self):
        request = self.factory.get('/dashboard/', HTTP_AUTHORIZATION=f'Bearer {self.student_access_token}')
        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # Assuming only one student data returned
