from django.db import models
from index.models import User

# Create your models here.


class Post(models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=250, default='No set')
	body = models.TextField()
	postType = models.CharField(max_length=100)
	category = models.CharField(max_length=100)
	edited = models.BooleanField(default=False)
	background = models.CharField(max_length=1000, default='na2.jpg')
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class Postcomment(models.Model):
	targetpost = models.ForeignKey(Post, default=1)
	author = models.ForeignKey(User, default='Anonymous')
	body = models.CharField(max_length=500)
	date = models.DateTimeField(auto_now=True)

