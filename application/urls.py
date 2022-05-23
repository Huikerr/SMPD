from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('smpd/', include('smpd.urls')),
    re_path('static/(?P<path>.*)', serve, {'document_root':settings.STATIC_ROOT}),
    re_path('media/(?P<path>.*)', serve, {'document_root':settings.MEDIA_ROOT})
]


