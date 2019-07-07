from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
	profilePics = models.FileField()
	aboutUser = models.TextField()
	numofnewnote = models.IntegerField(default=0)

	def __str__(self):
		return self.username
# 

from post.models import Post

class Following(models.Model):
	member = models.CharField(max_length=500, default='Anonymous')
	follow = models.ForeignKey(User, default='Anonymous')
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return (self.follow)


class View(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post, default='1')

	
class Wall(models.Model):
	user = models.CharField(max_length=500)
	writer = models.ForeignKey(User)
	body = models.TextField()
	date = models.DateTimeField(auto_now=True)

class WallReply(models.Model):
	wall = models.ForeignKey(Wall)
	body = models.CharField(max_length=500)
	writer = models.ForeignKey(User)
	date = models.DateTimeField(auto_now=True)


class Favour(models.Model):
	favouredBy = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	date = models.DateTimeField(auto_now=True)


class Notification(models.Model):
	user = models.ForeignKey(User)
	message = models.CharField(max_length=500)
	url = models.URLField(max_length=10000, default='/post')
	img = models.CharField(max_length=500, default='create.jpg')
	date = models.DateTimeField(auto_now=True)


class Likepage(models.Model):
	user = models.ForeignKey(User)
	fan = models.CharField(max_length=500) # username of the person that like your page
	date = models.DateTimeField(auto_now=True)


# class Description(models.Model):
# 	user = models.ForeignKey(User)
# 	body = models.TextField()

class Contact(models.Model):
	subject = models.CharField(max_length=1000)
	sender = models.CharField(max_length=500)
	email = models.CharField(max_length=500)
	message = models.TextField()
	date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.sender

class Quoteoftheday(models.Model):
	post = models.ForeignKey(Post)

	def __str__(self):
		return self.post.title


class Jokeoftheday(models.Model):
	post = models.ForeignKey(Post)

	def __str__(self):
		return self.post.title



class Motivationoftheday(models.Model):
	post = models.ForeignKey(Post)

	def __str__(self):
		return self.post.title


class Oneofakind(models.Model):
	post = models.ForeignKey(Post)

	def __str__(self):
		return self.post.title


class Selectionoftheday(models.Model):
	post = models.ForeignKey(Post)

	def __str__(self):
		return self.post.title
