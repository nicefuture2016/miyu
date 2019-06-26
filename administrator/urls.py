from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^sys_login/$', views.sys_login,name="sys_login"),
    url(r'^sys_logout/$', views.sys_logout,name="sys_logout"),

    # 术语
    url(r'^index$', views.index, name="index"),
    url(r'^parent/(\d+)/child/(\d+)/$', views.sys_child, name='sys_child'),
    url(r'^sys_shuyu_add/$', views.sys_shuyu_add, name='sys_shuyu_add'),
    url(r'^sys_shuyu_edit/(\d+)/$', views.sys_shuyu_edit, name='sys_shuyu_edit'),
    # 文章

    url(r'^article$', views.article, name="article"),
    url(r'^delarticle$', views.delarticle, name="delarticle"),
    url(r'^article/(\d+)/category/(\d+)/$', views.sys_lesson_child, name='sys_lesson_child'),
    url(r'^sys_article_add/(\d+)/$', views.sys_article_add, name='sys_article_add'),
    url(r'^sys_article_edit/(\d+)/$', views.sys_article_edit, name='sys_article_edit'),
]

