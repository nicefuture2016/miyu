from django.conf.urls import url, include
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
    url(r'^api/v1/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^administrator/', include('administrator.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
]
