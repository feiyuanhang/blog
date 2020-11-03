from django.shortcuts import render,redirect
import logging
from django.conf import settings
from app1.models import *
#文章分页处理
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

from django.db.models import Count

from app1.forms import *

from django.contrib.auth.views import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate
# Create your views here.

#1.1首网页展示
def index(request):
    try:
        # #1.分类信息的获取（导航栏数据）
        # category_list = Category.objects.all()
        # #2.广告数据（学生自己完成）
        # ad_list = Ad.objects.all()

        #3.最新文章数据
        article_list = Article.objects.all()
        # 分页代码设置
        article_list = paginator_list(request, article_list)

        # # 文章归档操作：（自定义objects 进行数据筛选）
        # archive_list = Article.objects.distinct_date()

    except Exception as e:
        logger.error(e)

    # return render(request,'index.html',{'category_list':category_list,'article_list':article_list,'ad_list':ad_list,})
    return render(request,'index.html',locals())


#1.2 文章归档页面编写
def archive(request):
    try:
        # # 1.分类信息的获取（导航栏数据）
        # category_list = Category.objects.all()
        # # 2.广告数据（学生自己完成）
        # ad_list = Ad.objects.all()
        # 3.归档文章数据
        #先提取客户端提交的信息

        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        article_list = Article.objects.filter(date_publish__icontains = year+'-'+month)

        #分页代码设置
        article_list = paginator_list(request,article_list)

        # # 文章归档操作：（自定义objects 进行数据筛选）
        # archive_list = Article.objects.distinct_date()
    except Exception as e:
        logger.error(e)
    return render(request, 'archive.html', locals())


#2.日志器的使用
logger = logging.getLogger('blog.views')


#3.全局上下文的使用：变量
def global_setting(request):
    SIIE_NAME = settings.SIIE_NAME
    SIIE_DESC = settings.SIIE_DESC
    CSDN = settings.CSDN
    # 1.分类信息的获取（导航栏数据）
    category_list = Category.objects.all()
    # 2.广告数据（学生自己完成）
    ad_list = Ad.objects.all()
    #3.标签云数据

    #4.文章归档
    # 文章归档操作：（自定义objects 进行数据筛选）
    archive_list = Article.objects.distinct_date()

    #5.友情链接数据


    #6.文章排行榜数据-评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count = Count('article')).order_by('-comment_count')   #分组聚合查询
    article_comment_list = [Article.objects.get(pk = comment['article']) for comment in comment_count_list]  #pk是主键的意思

    #----浏览排行
    click_count_list = Article.objects.order_by('-click_count')
    #----站长推荐-按评论
####################################

    return locals()


        # {'SIIE_NAME':settings.SIIE_NAME,
        #    'SIIE_DESC':settings.SIIE_DESC,
        #    'category_list':category_list,
        #    'ad_list':ad_list,
        #     'archive_list':archive_list,
        #    # 'MEDIA_ROOT':settings.MEDIA_ROOT,
        #    # 'MEDIA_URL':settings.MEDIA_URL,
        #    }
#4.分页函数
def paginator_list(request,article_list):
    paginator = Paginator(article_list, 2)
    try:
        # 获取当前页码
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)

    return article_list

#5.文章详情
def article(request):
    try:
        #获取文章id
        id = request.GET.get('id',None)

        try:
            #获取文章信息
            article = Article.objects.get(pk = id)

            # 阅读量 +1
            # a = article.objects.create(click_count = (article.click_count+1))     #说啥都不好用，之后成为大神后回来瞅瞅为啥嘞
            # a.save()

            # 阅读量 +1
            article.click_count1()         #竟然搞定了

        except Article.DoesNotExist:
            return render(request,'failure.html',{'reason':'没有找到对应文章'})

    #评论表单
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'url': request.user.url,
                                    'article': id} if request.user.is_authenticated() else{'article': id})
         # 获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id')
        comment_list = []
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'):
                    setattr(item, 'children_comment', [])
                if comment.pid == item:
                    item.children_comment.append(comment)
                    break
            if comment.pid is None:
                comment_list.append(comment)

    except Exception as e:
        logger.error(e)

    return render(request, 'article.html', locals())

# 提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data["author"],
                                             email=comment_form.cleaned_data["email"],
                                             url=comment_form.cleaned_data["url"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article"],
                                             user=request.user if request.user.is_authenticated() else None)
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注销
def do_logout(request):
    try:
        logout(request)          #
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

# 注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                # 注册
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                    email=reg_form.cleaned_data["email"],
                                    url=reg_form.cleaned_data["url"],
                                    password=make_password(reg_form.cleaned_data["password"]),)
                user.save()

                # 登录
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())

# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"]
                password = login_form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())

def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('cid', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = Article.objects.filter(category=category)
        article_list = paginator_list(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())


