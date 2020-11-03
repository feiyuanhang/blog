from django.urls import path
from app1 import views as app1_view

urlpatterns = [
    #首页展示
    path('index/',app1_view.index),

    # 文章归档url
    path('archive/', app1_view.archive),

    # 文章详情页面
    path('article/', app1_view.article),

# 文章详情页面
    path('login/', app1_view.do_login),

# 文章详情页面
    path('reg/', app1_view.do_reg),

# 文章详情页面
    path('logout/', app1_view.do_logout),

# 文章详情页面
    path('comment_post/', app1_view.comment_post),
]