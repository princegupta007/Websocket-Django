# # views.py
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.auth.hashers import make_password
# from django.db.models import Q

# # from .models import Admin_Student_mst, Admin_Teacher_mst
# # from .serializers import AdminStudentSerializer, AdminTeacherSerializer
# from account.models import CustomUser
# from account.serializers import UserSerializer


# @api_view(['POST'])
# def create_admin_student(request):
#     if request.method == 'POST':
#         serializer = AdminStudentSerializer(data=request.data)
#         if serializer.is_valid():
#             admin_student_data = serializer.validated_data

#             # Hash the password
#             admin_student_data['student_password'] = make_password(admin_student_data['student_password'])

#             # Save AdminStudent
#             admin_student = Admin_Student_mst.objects.create(**admin_student_data)

#             # Create CustomUser
#             CustomUser.objects.create(
#                 email=admin_student.student_email,
#                 username=admin_student.student_name,
#                 password=admin_student.student_password,
#                 user_type='student'
#             )
#             return Response({'message': 'student created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['POST'])
# def create_admin_teacher(request):
#     if request.method == 'POST':
#         serializer = AdminTeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             admin_teacher_data = serializer.validated_data

#             # Hash the password
#             admin_teacher_data['teacher_password'] = make_password(admin_teacher_data['teacher_password'])

#             # Save AdminTeacher
#             admin_teacher = Admin_Teacher_mst.objects.create(**admin_teacher_data)

#             # Create CustomUser
#             CustomUser.objects.create(
#                 email=admin_teacher.teacher_email,
#                 username=admin_teacher.teacher_name,
#                 password=admin_teacher.teacher_password,
#                 user_type='teacher'
#             )

#             return Response({'message': 'teacher created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         # Extract user_id from JWT token
#         user_id = request.user.id
#         print(user_id,"user_id")
#         user_type = request.user.user_type
#         print(user_type,"userType")

#         if user_type == 'superadmin':
#             queryset = CustomUser.objects.all()
#             print(queryset,"SUPER_ADMIN")

#         elif user_type == 'admin':
#             queryset = CustomUser.objects.filter(Q(user_type='teacher') | Q(user_type='student'))
#             print(queryset,"ADMIN")

#         elif user_type == 'teacher':
#             queryset = CustomUser.objects.filter(user_type='student')
#             print("Teacher")

#         elif user_type == 'student':
#             queryset = CustomUser.objects.filter(id=user_id)
#             print("STUDENT")
#         else:
#             queryset = CustomUser.objects.none()

#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)






# # views.py
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.hashers import make_password
# from .models import CustomUser, Admin, Teacher, Student
# from .serializers import AdminSerializer, TeacherSerializer, StudentSerializer

# @api_view(['POST'])
# def create_admin(request):
#     if request.method == 'POST':
#         serializer = AdminSerializer(data=request.data)
#         if serializer.is_valid():
#             admin = serializer.save()

#             # Create CustomUser
#             CustomUser.objects.create(
#                 email=admin.email,
#                 username=admin.username,
#                 password=make_password(admin.password),
#                 user_type='admin'
#             )

#             return Response({'message': 'Admin created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_teacher(request):
#     if request.method == 'POST':
#         serializer = TeacherSerializer(data=request.data)
#         if serializer.is_valid():
#             teacher = serializer.save()

#             # Create CustomUser
#             CustomUser.objects.create(
#                 email=teacher.email,
#                 username=teacher.username,
#                 password=make_password(teacher.password),
#                 user_type='teacher',
#                 parent_admin=teacher.admin_id
#             )

#             return Response({'message': 'Teacher created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_student(request):
#     if request.method == 'POST':
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid():
#             student = serializer.save()

#             # Create CustomUser
#             CustomUser.objects.create(
#                 email=student.email,
#                 username=student.username,
#                 password=make_password(student.password),
#                 user_type='student',
#                 parent_admin=student.teacher.admin_id
#             )

#             return Response({'message': 'Student created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






















# class DashboardView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         user_type = request.user.user_type
#         user_id = request.user.id

#         if user_type == 'superadmin':
#             # For superadmin, count total admin, teacher, and student
#             admin_count = CustomUser.objects.filter(user_type='admin').count()
#             teacher_count = CustomUser.objects.filter(user_type='teacher').count()
#             student_count = CustomUser.objects.filter(user_type='student').count()
#             return Response({
#                 'admin_count': admin_count,
#                 'teacher_count': teacher_count,
#                 'student_count': student_count
#             }, status=status.HTTP_200_OK)
        
#         elif user_type == 'admin':
#             # For admin, count total teachers and students
#             teacher_count = CustomUser.objects.filter(parent_admin=user_id, user_type='teacher').count()
#             student_count = CustomUser.objects.filter(parent_admin=user_id, user_type='student').count()
#             return Response({
#                 'teacher_count': teacher_count,
#                 'student_count': student_count
#             }, status=status.HTTP_200_OK)
        
#         elif user_type == 'teacher':
#             # For teacher, count total students
#             student_count = CustomUser.objects.filter(parent_admin=user_id, user_type='student').count()
#             return Response({
#                 'student_count': student_count
#             }, status=status.HTTP_200_OK)
        
#         elif user_type == 'student':
#             # For student, retrieve only the student's own data
#             student_data = CustomUser.objects.filter(id=user_id)
#             serializer = UserSerializer(student_data, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         else:
#             # For other user types, return empty response
#             return Response({}, status=status.HTTP_400_BAD_REQUEST)





























from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password
from .models import Admin_mst, User_mst
from account.models import  CustomUser
from .serializers import AdminSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_admin(request):
    if request.method == 'POST':
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin_data = serializer.validated_data

             # Extract superadmin_id from request data
            superadmin_id = admin_data.pop('superadmin').id  # Change 'superadmin_id' to the actual key name
            print(superadmin_id,"superadmin_id.................________________________________")

            # Hash the password
            admin_data['admin_password'] = make_password(admin_data['admin_password'])

            # Save Admin
            admin = Admin_mst.objects.create(**admin_data, superadmin_id=superadmin_id)

            # Create CustomUser
            CustomUser.objects.create(
                email=admin.admin_email,
                first_name=admin.admin_firstname,
                last_name=admin.admin_lastname,
                username=admin.admin_username,
                password=admin.admin_password,
                parent_admin_id=superadmin_id,
                user_type='admin',
            )
            return Response({'message': 'Admin created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data

            # Extract admin_id from request data
            admin_id = user_data.pop('admin').id  # Remove 'admin' from user_data and get the admin ID

            user_data['user_password'] = make_password(user_data['user_password'])

            # Save User
            user = User_mst.objects.create(**user_data, admin_id=admin_id)

            # Assuming CustomUser has these fields, modify accordingly if needed
            CustomUser.objects.create(
                email=user.user_email,
                first_name=user.user_firstname,
                last_name=user.user_lastname,
                username=user.user_username,
                password=user.user_password,
                parent_admin_id=admin_id,  # Assigning admin id here
                user_type='user',
            )

            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_type = request.user.user_type
        user_id = request.user.id
        print("user_type:",user_type,"|user_id:",user_id) 
        username = request.user.username

        if user_type == 'superadmin':
            # Fetch admin count and data
            admins = Admin_mst.objects.all()
            admin_count = admins.count()
            admin_data = AdminSerializer(admins, many=True).data

            # Fetch user count and data
            users = User_mst.objects.all()
            user_count = users.count()
            user_data = UserSerializer(users, many=True).data

            return Response({
                'admin_count': admin_count,
                'admins': admin_data,
                'user_count': user_count,
                'users': user_data
            }, status=status.HTTP_200_OK)

        elif user_type == 'admin':
             # Fetch admin count and data based on the username
            admins = Admin_mst.objects.filter(admin_username=username)
            admin_data = AdminSerializer(admins, many=True).data

            # Fetch user count and data for users under this admin
            users = User_mst.objects.filter(admin_id=user_id)
            user_count = users.count()
            user_data = UserSerializer(users, many=True).data      

            return Response({
                'admin_count': admin_count,
                'admins': admin_data,
                'user_count': user_count,
                'users': user_data
            }, status=status.HTTP_200_OK)

        elif user_type == 'user':
            # Fetch user data for users
            users = User_mst.objects.filter(user_username=username)
            user_data = UserSerializer(users, many=True).data   

            return Response({
                # 'admin_count': [0],
                # 'admins': ['null'],
                # 'user_count': [0],
                'users': user_data
            }, status=status.HTTP_200_OK)


        else:
            # For other user types, return empty response
            return Response({}, status=status.HTTP_400_BAD_REQUEST)