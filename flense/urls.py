from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
	url(r'^', include('index.urls')),
	url(r'^api/', include('api.urls')),
	url(r'^post/', include('post.urls')),
    url(r'^admin/', admin.site.urls),
]
