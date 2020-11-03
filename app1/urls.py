from django.urls import path
from app1 import views as app1_view

urlpatterns = [
    #��ҳչʾ
    path('index/',app1_view.index),

    # ���¹鵵url
    path('archive/', app1_view.archive),

    # ��������ҳ��
    path('article/', app1_view.article),

# ��������ҳ��
    path('login/', app1_view.do_login),

# ��������ҳ��
    path('reg/', app1_view.do_reg),

# ��������ҳ��
    path('logout/', app1_view.do_logout),

# ��������ҳ��
    path('comment_post/', app1_view.comment_post),
]