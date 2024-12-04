from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Role(models.Model):
    nama_role = models.CharField(max_length=50, unique=True)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.nama_role
    

class KategoriMotor(models.Model):
    nama_kategori = models.CharField(max_length=100)
    keterangan = models.TextField(blank=True)

    def __str__(self):
        return self.nama_kategori


class User(AbstractUser):
    access_level = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set_permissions',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username


class Motor(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  
    nama_motor = models.CharField(max_length=100)
    merk = models.CharField(max_length=50)
    harga = models.FloatField()
    stok = models.IntegerField()
    keterangan = models.TextField(blank=True)
    gambar = models.ImageField(upload_to='motor_images/', blank=True, null=True)
    kategori_motor = models.ForeignKey(KategoriMotor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nama_motor
