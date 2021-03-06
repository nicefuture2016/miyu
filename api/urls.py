from django.conf.urls import  url
from . import views
from rest_framework.routers import DefaultRouter
#from rest_framework_jwt.views import obtain_jwt_token

#router = DefaultRouter()

#router.register(r'shuyu', views.ShuYuViewSet, base_name='shuyu')

urlpatterns = [
    # 主页
    # 获取banner
    url(r'^banner/$', views.Banner.as_view(), name='banner'),
    # 主页文章
    url(r'^home/$', views.HomeView.as_view(), name='home'),
    # 术语搜索
    url(r'^search/$', views.ShuYuSearchView.as_view(), name='search'),
    # 恋爱话术总分类
    url(r'^category/$', views.ParentView.as_view(), name='category'),
    # 恋爱话术子分类
    url(r'^category/child/$', views.ChildView.as_view(), name='child'),
    # 主页分类课程
    url(r'^zyflkc/$', views.ZYFLKCView.as_view(), name='zyflkc'),
    # 搜索排行榜
    url(r'^topsearch/$', views.SearchRank.as_view(), name='topsearch'),

    # 教程
    # 教程分类
    url(r'^lesson/$', views.ParentLessonView.as_view(), name='lesson'),
    # 教程子分类列表
    url(r'^lesson/child/$', views.ChildLessonView.as_view()),
    # 教程子分类文章列表
    url(r'^lesson/child/list/$', views.ChildLessonListView.as_view()),
    # 获取课程内容
    url(r'^lesson/content/$', views.LessonContentView.as_view()),
    # 喜欢
    url(r'^lesson/like/$', views.LessonLikeView.as_view()),
    # 收藏
    url(r'^lesson/favorite/$', views.LessonFavoriteView.as_view()),
    # 我的收藏
    url(r'^lesson/myfavorite/$', views.LessonMyFavoriteView.as_view()),

    # 我的
    # 登录
    url(r'^auth/', views.LoginView.as_view(),name='auth'),
    # 获取验证码
    url(r'^getcode/$', views.GetSmsCodeView.as_view(), name='getcode'),
    # 提交反馈
    url(r'^question/$', views.QuestionView.as_view(), name='question'),
    url(r'^data/$', views.data, name='data'),


]
#+ router.urls
