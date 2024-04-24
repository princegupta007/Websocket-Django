# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class CustomUser(AbstractUser):
#     SUPERADMIN = 'superadmin'
#     ADMIN = 'admin'
#     TEACHER = 'teacher'
#     STUDENT = 'student'

#     USER_TYPE_CHOICES = [
#         (SUPERADMIN, 'Super Admin'),
#         (ADMIN, 'Admin'),
#         (TEACHER, 'teacher'),
#         (STUDENT, 'student'),
#     ]

#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=STUDENT)


# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    USER = 'user'

    USER_TYPE_CHOICES = [
        (SUPERADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (USER, 'user'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER)
    parent_admin = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
