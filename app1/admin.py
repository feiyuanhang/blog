from django.contrib import admin
from app1.models import *
# Register your models here.

#自定义一个管理类
class ArticleAdmin(admin.ModelAdmin):
    fields = ('title','desc','content','user','tag','category')

    class Media:
        js = (
            '/static/js/kindeditor-4.1.10/kindeditor-min.js',
            '/static/js/kindeditor-4.1.10/lang/zh_CN.js',
            '/static/js/kindeditor-4.1.10/config.js',
        )

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Article,ArticleAdmin,)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Links)
admin.site.register(Ad)