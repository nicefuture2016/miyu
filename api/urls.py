from django.conf.urls import  url
from . import views
from rest_framework.routers import DefaultRouter
#from rest_framework_jwt.views import obtain_jwt_token

#router = DefaultRouter()

#router.register(r'shuyu', views.ShuYuViewSet, base_name='shuyu')

urlpatterns = [
    url(r'^category/$', views.ParentView.as_view(), name='category'),
    url(r'^child/(?P<pk>\d+)/$', views.ChildView.as_view(), name='child'),
    url(r'^topsearch/$', views.SearchRank.as_view(), name='topsearch'),
    url(r'^shuyu/$', views.ShuYuSearchView.as_view(), name='shuyu'),
    url(r'^lesson/$', views.ParentLessonView.as_view(), name='lesson'),
    url(r'^lesson/(?P<pk>\d+)/cid/(?P<cid>\d+)/$', views.ChildLessonView.as_view()),
    url(r'^lesson/content/(?P<pk>\d+)/$', views.LessonContentView.as_view()),
    url(r'^lesson/like/(?P<pk>\d+)/$', views.LessonLikeView.as_view()),
    url(r'^lesson/favorite/$', views.LessonFavoriteView.as_view()),
    url(r'^lesson/myfavorite/$', views.LessonMyFavoriteView.as_view()),
    url(r'^auth/', views.LoginView.as_view(),name='auth'),
    url(r'^getcode/$', views.GetSmsCodeView.as_view(), name='getcode'),
    url(r'^banner/$', views.Banner.as_view(), name='banner'),
    url(r'^data/$', views.data, name='data'),
]
#+ router.urls
