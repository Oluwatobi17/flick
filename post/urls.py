from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.posts, name='posts'),

	# Listing all post of postType=type
	url(r'^(?P<postType>[a-zA-Z]+)/all/$', views.posts, name='myposts'),

	# Getting a single post with id=post_id
	url(r'^(?P<post_id>[0-9]+)/$', views.a_post, name='one_post'),
]