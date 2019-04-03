from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^wall/$', views.WallList.as_view(), name='wall'),
	url(r'^following/$', views.Following.as_view(), name='following'),
]

urlpatterns = format_suffix_patterns(urlpatterns)