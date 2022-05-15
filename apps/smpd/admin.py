from django.contrib import admin
from smpd.models import Camera
from django.contrib.auth.models import Group
# Register your models here.

class CameraAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','code','username','password','url','status')
    list_per_page = 20


admin.site.register(Camera, CameraAdmin)
admin.site.unregister(Group)


admin.site.site_title = "屏幕监测平台"
admin.site.site_header = "屏幕监测平台"
admin.site.index_title = "欢迎来到屏幕监测平台"



