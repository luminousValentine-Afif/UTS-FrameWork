from django.contrib import admin
from .models import Item, Role, KategoriMotor, Motor, User

# Tidak perlu unregister User dan Group karena kita menggunakan model User kustom
admin.site.register(Item)
admin.site.register(Role)
admin.site.register(KategoriMotor)
admin.site.register(Motor)
admin.site.register(User)