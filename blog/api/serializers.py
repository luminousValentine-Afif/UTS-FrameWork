from rest_framework import serializers
from . import models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ['id', 'nama_role', 'keterangan']  # Menambahkan id, nama_role, dan keterangan



class UserSerializer(serializers.ModelSerializer):
    access_level = serializers.PrimaryKeyRelatedField(queryset=models.Role.objects.all(), allow_null=True)
    access_level_display = serializers.StringRelatedField(source='access_level')

    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Menghindari password muncul dalam response
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
class MotorSerializer(serializers.ModelSerializer):
    kategori_motor = serializers.PrimaryKeyRelatedField(queryset=models.KategoriMotor.objects.all())
    kategori_motor_display = serializers.StringRelatedField(source='kategori_motor')
    gambar = serializers.ImageField(use_url=True)
    user = serializers.StringRelatedField(read_only=True)  # Menampilkan nama user

    class Meta:
        model = models.Motor
        fields = '__all__'

    def create(self, validated_data):
        if 'request' not in self.context:
            raise ValueError("Context 'request' tidak ditemukan.")
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


        
class KategoriMotorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KategoriMotor
        fields = '__all__'
