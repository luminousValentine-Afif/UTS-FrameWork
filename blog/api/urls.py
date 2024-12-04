from django.urls import path
from . import views
from rest_framework.routers  import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user/', views.User_List.as_view(), name='user_list'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('user-profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('roles/', views.RoleList.as_view(), name='role_list'),

    path('motor/', views.Motor_List.as_view(), name='motor_list'),
    path('motors/<int:pk>/', views.MotorDetail.as_view(), name='motor_detail'),
    path('kategori-motor/', views.KategoriMotor_List.as_view(), name='kategori_motor_list'),
    path('kategori-motor/<int:pk>/', views.KategoriMotorDetail.as_view(), name='kategori_motor_detail'),
]
