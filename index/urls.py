from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^notification/$', views.notification, name='notification'),
	url(r'^profile/$', views.myprofile, name='myprofile'),
	url(r'^profile/(?P<username>[a-zA-Z]+)$', views.a_user, name='one_user'),
	url(r'^sign-in/$', views.login, name='login'),
	url(r'^sign-up/$', views.register, name='register'),
	url(r'^sign-out/$', views.logout, name='logout'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^follow/(?P<username>[a-zA-Z]+)$', views.follow, name='follow'),
	url(r'^unfollow/(?P<username>[a-zA-Z]+)$', views.unfollow, name='unfollow'),
	url(r'^update/password/$', views.changepassword, name='changepassword'),
	url(r'^update/editprofile/$', views.editprofile, name='editprofile'),
	url(r'^wall/writeon/(?P<username>[a-zA-Z]+)/$', views.writeonwall, name='writeonwall'),
	url(r'^wall/writereply/(?P<wall_id>[0-9]+)/$', views.writewallreply, name='writewallreply'),
	url(r'^likepage/(?P<username>[a-zA-Z]+)/$', views.likepage, name='likepage'),
	url(r'^checknotification/$', views.checknotification, name='checknotification'),
	
]