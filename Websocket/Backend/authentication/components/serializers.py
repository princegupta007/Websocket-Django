from rest_framework import serializers
from .models import Admin_mst, User_mst

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin_mst
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_mst
        fields = '__all__'




# # serializers.py
# from rest_framework import serializers
# from .models import Admin, Teacher, Student

# class AdminSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Admin
#         fields = '__all__'

# class TeacherSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Teacher
#         fields = '__all__'

# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = '__all__'