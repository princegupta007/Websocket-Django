from django.db import models
from account.models import  CustomUser

class Admin_mst(models.Model):
    admin_username = models.CharField(max_length=100,unique=True,null=False,blank=False)
    admin_firstname = models.CharField(max_length=100)
    admin_lastname = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_mobile = models.CharField(max_length=15)
    admin_password = models.CharField(max_length=100, null=True, blank=True)
    superadmin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='admin')

class User_mst(models.Model):
    user_username = models.CharField(max_length=100,unique=True,null=False,blank=False)
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    user_mobile = models.CharField(max_length=15)
    user_password = models.CharField(max_length=100, null=True, blank=True) 
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')






# class Admin(models.Model):
#     # Add fields specific to admin

# class Admin_mst(models.Model):
#     # Add fields specific to teacher
#     admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='teachers')

# class User_mst(models.Model):
#     # Add fields specific to student
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')
