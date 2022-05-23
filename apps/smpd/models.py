from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from uuid import uuid4
from django.conf import settings
import os, shutil
# Create your models here.

class UserProfile(AbstractUser):
    name = models.CharField(max_length=255, null=True, verbose_name="名称",default="SMPDAdmin") # 名称
    class Meta:
        db_table = "tb_user"
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        ordering = ('id', )
    def __str__(self):
        return f"{self.name}"

class Camera(Model):
    name = models.CharField(max_length=255, default="网络摄像头", verbose_name="摄像头")
    code = models.CharField(max_length=255, null=True, verbose_name="编码", blank=True,default=uuid4)
    username = models.CharField(max_length=255, null=True, verbose_name="账号", blank=True,default="admin")
    password = models.CharField(max_length=255, null=True, verbose_name="密码", blank=True,default="a123123123")
    status = models.BooleanField(verbose_name="状态",help_text="状态", default=False)
    rtsp = models.CharField(max_length=255, null=True, verbose_name="地址",
                            blank=True,default="rtsp://admin:a123123123@192.168.1.64:554/h265/ch1/main/av_stream")
    ip = models.CharField(max_length=255, null=True, verbose_name="IP", blank=True,default="192.168.1.64:554")
    port = models.CharField(max_length=255, null=True, verbose_name="端口号", blank=True, default="554")
    path = models.CharField(max_length=255, null=True, blank=True, verbose_name="路径", help_text="配置路径")

    # 自定义保存
    def save(self, *args, **kwargs):
        if self.path is None:
            self.path = 'camera/{}'.format(self.code)
            os.makedirs(os.path.join(settings.MEDIA_ROOT, self.path))
        else:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, self.path)):
                pass
            else:
                os.makedirs(os.path.join(settings.MEDIA_ROOT, self.path))
        if self.username and self.password and self.ip and self.port is None:
            pass
        else:
            self.rtsp = "rtsp://{}:{}@{}:{}/h265/ch1/main/av_stream".format(str(self.username),str(self.password),str(self.ip),str(self.port))
        return super().save(*args, **kwargs)

    # 自定义删除
    def delete(self, *args, **kwargs):
        if os.path.exists(os.path.join(settings.MEDIA_ROOT, self.path)):
                shutil.rmtree(os.path.join(settings.MEDIA_ROOT, self.path))
        else:
            pass
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = "tb_camera"
        verbose_name = '摄像头管理'
        verbose_name_plural = verbose_name
        ordering = ('id', )
    def __str__(self):
        return f"{self.name}"

    def label(self):
        parameter_str = 'id={}'.format(str(self.id))
        color_code = ''
        btn_str = '<a class="btn btn-xs btn-danger" href="{}">' \
                  '<input name="标注"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="标注">' \
                  '</a>'
        data = {'id': self.id}
        return format_html(btn_str, '/smpd/label/?id={}'.format(str(self.id)), kwargs=str(self.id))
    label.allow_tags = True
    label.short_description = '标注框'

    def view(self):
        parameter_str = 'id={}'.format(str(self.id))
        color_code = ''
        btn_str = '<a href="{}">' \
                  '<input name="查看"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="查看">' \
                  '</a>'
        return format_html(btn_str, '/smpd/view/?{}'.format(parameter_str))
    view.allow_tags = True
    view.short_description = '摄像头'

    def record(self):
        parameter_str = 'id={}'.format(str(self.id))
        btn_str = '<a class="layui-icon layui-icon-video" href="{}">' \
                  '<input name="录制"' \
                  'type="button" id="passButton" ' \
                  'title="passButton" value="录制">' \
                  '</a>'
        return format_html(btn_str, '/smpd/record/?{}'.format(parameter_str))
    record.allow_tags = True
    record.short_description = '查看视频'