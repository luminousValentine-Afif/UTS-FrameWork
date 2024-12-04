from rest_framework.permissions import BasePermission
from . import views

class IsAdmin(BasePermission):
    """
    Izinkan akses hanya untuk Admin.
    """
    def has_permission(self, request, view):
        return request.user.access_level.nama_role == 'Admin'

class IsStaff(BasePermission):
    """
    Izinkan akses hanya untuk Staff.
    """
    def has_permission(self, request, view):
        return request.user.access_level.nama_role == 'Staff'

class IsView(BasePermission):
    """
    Izinkan akses hanya untuk View, tetapi tidak dapat melihat daftar pengguna.
    """
    def has_permission(self, request, view):
        user_role = request.user.access_level.nama_role
        
        if user_role == 'View':
            if isinstance(view, views.User_List):
                return False  # View tidak dapat melihat daftar pengguna

        return True
