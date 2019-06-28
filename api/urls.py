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
    # 术语搜索
    url(r'^search/$', views.ShuYuSearchView.as_view(), name='search'),
    # 恋爱话术总分类
    url(r'^category/$', views.ParentView.as_view(), name='category'),
    # 恋爱话术子分类
    url(r'^category/child/$', views.ChildView.as_view(), name='child'),
    # 网上撩妹&聊天教学
    url(r'^ltjx/$', views.LTJXView.as_view(), name='ltjx'),
    # 每日优选
    url(r'^mrjx/$', views.MRJXView.as_view(), name='mrjx'),
    # 课程推荐
    url(r'^kctj/$', views.KCTJView.as_view(), name='kctj'),
    # 主页分类课程
    url(r'^zyflkc/$', views.ZYFLKCView.as_view(), name='zyflkc'),

    url(r'^topsearch/$', views.SearchRank.as_view(), name='topsearch'),

    url(r'^lesson/$', views.ParentLessonView.as_view(), name='lesson'),
    url(r'^lesson/(?P<pk>\d+)/cid/(?P<cid>\d+)/$', views.ChildLessonView.as_view()),
    url(r'^lesson/content/(?P<pk>\d+)/$', views.LessonContentView.as_view()),
    url(r'^lesson/like/(?P<pk>\d+)/$', views.LessonLikeView.as_view()),
    url(r'^lesson/favorite/$', views.LessonFavoriteView.as_view()),
    url(r'^lesson/myfavorite/$', views.LessonMyFavoriteView.as_view()),
    url(r'^auth/', views.LoginView.as_view(),name='auth'),
    url(r'^getcode/$', views.GetSmsCodeView.as_view(), name='getcode'),

    url(r'^data/$', views.data, name='data'),


]
#+ router.urls
