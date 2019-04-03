from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.posts, name='posts'),

	# Listing all post of postType=type
	url(r'^(?P<postType>[a-zA-Z]+)/all/$', views.posts, name='myposts'),

	# Getting a single post with id=post_id
	url(r'^(?P<post_id>[0-9]+)/$', views.a_post, name='one_post'),

	# For edit a post with id=post_id
	url(r'^(?P<post_id>[0-9]+)/editpost/$', views.editpost, name='editpost'),

	# Give a comment to a post
	url(r'^(?P<post_id>[0-9]+)/givecomment/$', views.givecomment, name='givecomment'),

	# Creating a new post
	url(r'^createpost/$', views.createpost, name='createpost'),

	# /favour a post with pk=post_id
	url(r'^favour/(?P<post_id>[0-9]+)/$', views.favourpost, name='favourpost'),

	# /unfavour a post with pk=post_id
	url(r'^unfavour/(?P<post_id>[0-9]+)/$', views.unfavourpost, name='unfavourpost'),
]