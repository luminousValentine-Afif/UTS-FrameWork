from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from .serializers import UserSerializer, MotorSerializer, KategoriMotorSerializer, RoleSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsStaff, IsView

class RoleList(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]  # Setiap pengguna harus terautentikasi

        user_role = self.request.user.access_level.nama_role

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa melihat, menambah, mengubah, dan menghapus role
        else:
            return []  # Staff dan View tidak bisa mengakses daftar role sama sekali

        return permissions

    def get(self, request):
        # Hanya Admin yang bisa melihat daftar role
        if request.user.access_level.nama_role == 'Admin':
            roles = models.Role.objects.all()
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data)

        return Response({"detail": "You do not have permission to view the role list."}, status=403)

    def post(self, request):
        # Hanya Admin yang bisa menambah role
        if request.user.access_level.nama_role != 'Admin':
            return Response({"detail": "You do not have permission to add roles."}, status=403)

        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class User_List(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        user_role = self.request.user.access_level.nama_role

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa melihat semua pengguna
        elif user_role == 'Staff':
            permissions.append(IsStaff())  # Staff hanya bisa melihat data mereka sendiri
        elif user_role == 'View':
            return []  # View tidak bisa melihat daftar pengguna

        return permissions

    def get(self, request):
        if request.user.access_level.nama_role == 'Admin':
            users = models.User.objects.all()  # Menggunakan models.User
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        # Staff hanya bisa melihat data mereka sendiri
        if request.user.access_level.nama_role == 'Staff':
            users = models.User.objects.filter(id=request.user.id)  # Hanya data mereka sendiri
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        return Response({"detail": "You do not have permission to view the user list."}, status=403)

    def post(self, request):
        if request.user.access_level.nama_role != 'Admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        user_role = self.request.user.access_level.nama_role

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa melihat dan mengedit pengguna
        elif user_role == 'Staff':
            permissions.append(IsStaff())  # Staff hanya bisa melihat data mereka sendiri
        elif user_role == 'View':
            return []  # View tidak bisa melihat detail pengguna

        return permissions

    def get(self, request, pk):
        try:
            user = models.User.objects.get(id=pk)  # Menggunakan models.User
        except models.User.DoesNotExist:
            return Response({"detail": "User not found."}, status=404)

        # Hanya Admin yang bisa melihat detail pengguna lain
        if request.user.access_level.nama_role == 'Admin':
            serializer = UserSerializer(user)
            return Response(serializer.data)

        # Staff hanya bisa melihat data mereka sendiri
        if request.user.access_level.nama_role == 'Staff' and user.id == request.user.id:
            serializer = UserSerializer(user)
            return Response(serializer.data)

        return Response({"detail": "You do not have permission to view this user's details."}, status=403)

    def put(self, request, pk):
        # Hanya Admin yang bisa melakukan update
        if request.user.access_level.nama_role != 'Admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = models.User.objects.get(id=pk)  # Menggunakan models.User
        except models.User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)  # partial=True untuk update parsial
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Hanya Admin yang bisa melakukan delete
        if request.user.access_level.nama_role != 'Admin':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = models.User.objects.get(id=pk)  # Menggunakan models.User
        except models.User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Periksa apakah pengguna yang sedang login mencoba menghapus dirinya sendiri
        if user == request.user:
            return Response({"detail": "You cannot delete your own account."}, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({"detail": "User successfully deleted."}, status=status.HTTP_204_NO_CONTENT)

    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_level": {
                "id": user.access_level.id,
                "nama_role": user.access_level.nama_role,
            },
        }
        return Response(data)

#yang baru
class Motor_List(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]  # Set permission default
        user_role = self.request.user.access_level.nama_role  # Ambil role pengguna

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa semua operasi
        elif user_role == 'Staff':
            permissions.append(IsStaff())  # Staff bisa lihat dan update, tapi tidak delete
        elif user_role == 'View':
            permissions = [IsAuthenticated(), IsView()]  # View hanya bisa melakukan GET motor

        return permissions

    def get(self, request):
        motors = models.Motor.objects.all()
        serializer = MotorSerializer(motors, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_role = request.user.access_level.nama_role
        if user_role == 'Admin' or user_role == 'Staff':
            # Perubahan di sini: Sertakan 'request' dalam context saat membuat serializer
            serializer = MotorSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # Menyimpan data motor dengan user yang diambil dari request
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

class MotorDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]  # Set permission default
        user_role = self.request.user.access_level.nama_role  # Ambil role pengguna

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa semua operasi
        elif user_role == 'Staff':
            permissions.append(IsStaff())  # Staff bisa lihat dan update, tapi tidak delete
        elif user_role == 'View':
            permissions = [IsAuthenticated(), IsView()]  # View hanya bisa melihat detail motor

        return permissions

    def get(self, request, pk):
        try:
            motor = models.Motor.objects.get(id=pk)
            serializer = MotorSerializer(motor)
            return Response(serializer.data)
        except models.Motor.DoesNotExist:
            return Response({"detail": "Motor not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            motor = models.Motor.objects.get(id=pk)

            # Perubahan di sini: Jika user bukan admin/staff, hanya pemilik yang bisa update
            if motor.user != request.user and request.user.access_level.nama_role not in ['Admin', 'Staff']:
                return Response({"detail": "You can only update your own motor."}, status=status.HTTP_403_FORBIDDEN)

            serializer = MotorSerializer(motor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()  # Update motor dengan data yang baru
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except models.Motor.DoesNotExist:
            return Response({"detail": "Motor not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user_role = request.user.access_level.nama_role
        if user_role != 'Admin' and user_role != 'Staff':
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        try:
            motor = models.Motor.objects.get(id=pk)

            # Perubahan di sini: Jika user bukan admin/staff, hanya pemilik yang bisa delete
            if motor.user != request.user and user_role not in ['Admin', 'Staff']:
                return Response({"detail": "You can only delete your own motor."}, status=status.HTTP_403_FORBIDDEN)

            motor.delete()  # Hapus motor
            return Response({"detail": "Motor successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except models.Motor.DoesNotExist:
            return Response({"detail": "Motor not found."}, status=status.HTTP_404_NOT_FOUND)



class KategoriMotor_List(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]  # Set permission default
        user_role = self.request.user.access_level.nama_role  # Ambil role pengguna

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa semua operasi
        elif user_role == 'Staff':
            permissions.append(IsStaff())  # Staff bisa lihat dan update, tapi tidak delete
        elif user_role == 'View':
            # View tidak bisa melihat kategori motor
            return []  # Tidak ada permissions untuk View di KategoriMotor_List

        return permissions

    def get(self, request):
        kategorimotors = models.KategoriMotor.objects.all()
        serializer = KategoriMotorSerializer(kategorimotors, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_role = request.user.access_level.nama_role
        if user_role == 'Admin' or user_role == 'Staff':
            serializer = KategoriMotorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

class KategoriMotorDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        permissions = [IsAuthenticated()]  # Set permission default
        user_role = self.request.user.access_level.nama_role  # Ambil role pengguna

        if user_role == 'Admin':
            permissions.append(IsAdmin())  # Admin bisa semua operasi
        elif user_role == 'Staff':
            permissions.append(IsStaff())  # Staff bisa lihat dan update, tapi tidak delete
        elif user_role == 'View':
            # View tidak bisa melihat atau mengubah kategori motor
            return []  # Tidak ada permissions untuk View di KategoriMotorDetail

        return permissions

    def get(self, request, pk):
        kategorimotor = models.KategoriMotor.objects.get(id=pk)
        serializer = KategoriMotorSerializer(kategorimotor)
        return Response(serializer.data)

    def put(self, request, pk):
        kategorimotor = models.KategoriMotor.objects.get(id=pk)
        if request.user.access_level.nama_role in ['Admin', 'Staff']:
            serializer = KategoriMotorSerializer(kategorimotor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        kategorimotor = models.KategoriMotor.objects.get(id=pk)
        if request.user.access_level.nama_role == 'Admin' or request.user.access_level.nama_role == 'Staff':
            kategorimotor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
