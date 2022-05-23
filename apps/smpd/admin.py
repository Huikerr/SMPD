from django.contrib import admin
from smpd.models import Camera,UserProfile
from django.contrib.auth.models import Group
# Register your models here.

class CameraAdmin(admin.ModelAdmin):
    list_display = ('name',  'username', 'password', 'ip', 'port', 'status', 'view', 'label')
    list_per_page = 20
    list_editable = ('username', 'password', 'ip', 'port', 'status')
    search_fields = ('name', 'id')

    # # 自定义按钮
    # actions = ['test']

    # def test(self, request, queryset):
    #     pass

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','username','password')
    list_per_page = 20

admin.site.register(Camera, CameraAdmin)
admin.site.unregister(Group)
# admin.site.register(UserProfile,UserProfileAdmin )


admin.site.site_title = "屏幕监测平台"
admin.site.site_header = "屏幕监测平台"
admin.site.index_title = "欢迎来到屏幕监测平台"



