"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from blog import  settings
#上传图片
from app1.upload import upload_image
from django.views import static



urlpatterns = [

    path('admin/', admin.site.urls),
    path('app1/',include('app1.urls')),

    #其他位置上传照片处理
    re_path(r'uploads/(?P<path>.*)', static.serve, {"document_root": settings.MEDIA_ROOT}),

    #富文本编辑器上传照片问题
    re_path(r'admin/upload/(?P<dir_name>[^/]+)', upload_image, name='upload_image'),

]

