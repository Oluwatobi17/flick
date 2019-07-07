from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^mywall/$', views.WallList.as_view(), name='wall'),
	url(r'^fellowship/(?P<action>[a-zA-Z]+)/(?P<username>[a-zA-Z]+)/$', views.FollowingApi.as_view(), name='following'),
	url(r'^favouring/(?P<action>[a-zA-Z]+)/(?P<post_id>[0-9]+)/$', views.FavourPost.as_view(), name='favouring'),
	url(r'^replywall/$', views.ReplyWallpost.as_view(), name='replywallpost'),
	url(r'^editpost/(?P<post_id>[0-9]+)/$', views.Editpost.as_view(), name='editpost'),
	url(r'^commentpost/$', views.Commentpost.as_view(), name='commentpost'),
	url(r'^addpost/$', views.Addpost.as_view(), name='addtpost'),
	url(r'^likepage/(?P<username>[a-zA-Z]+)/$', views.LikePage.as_view(), name='likepage'),
	url(r'^checknotification/$', views.Checknotification.as_view(), name='checknotification'),
	url(r'^contact/$', views.Contact.as_view(), name='contact'),
	url(r'^searchUsername/$', views.SearchUsername.as_view(), name='searchusername'),
	url(r'^searchPost/$', views.SearchPost.as_view(), name='searchpost'),

]

urlpatterns = format_suffix_patterns(urlpatterns)