from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    name = models.CharField(max_length=255, null=True, verbose_name="名称",default="user") # 名称
    class Meta:
        db_table = "tb_user"
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        ordering = ('id', )
    def __str__(self):
        return f"{self.name}"

class Camera(models.Model):
    name = models.CharField(max_length=255, default="网络摄像头", verbose_name="摄像头")
    code = models.CharField(max_length=255, null=True, verbose_name="编码", blank=True,default="123456789")
    username = models.CharField(max_length=255, null=True, verbose_name="账号", blank=True,default="admin")
    password = models.CharField(max_length=255, null=True, verbose_name="密码", blank=True,default="a123123123")
    status = models.BooleanField(verbose_name="状态",help_text="状态", default=0)
    url = models.CharField(max_length=255, null=True, verbose_name="地址", blank=True,default="rtsp://admin:a123123123@192.168.1.64:554/h265/ch1/main/av_stream")
    class Meta:
        db_table = "tb_camera"
        verbose_name = '摄像头管理'
        verbose_name_plural = verbose_name
        ordering = ('id', )
    def __str__(self):
        return f"{self.name}"