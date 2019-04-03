from django.shortcuts import render, redirect
from post.models import Post, Postcomment
from .forms import EditPost, CommentPost, CreateNewPost
from index.models import User, Favour, Following, View, Notification
from django.contrib import messages
import random

# Create your views here.

def posts(request, postType):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else:
		user = User.objects.get(username=request.user.username)
		following = []
		for followMem in Following.objects.filter(member=request.user.username):
			following.append(followMem.follow.username)

		if Post.objects.filter(postType=postType):
			return render(request, 'post/posts.html', {
				'title': 'List of '+postType,
				'posts': Post.objects.filter(postType=postType).order_by('-date'),
				'postType': postType,
				'authentication': True,
				'user': user,
				'following': following,
				'notification': Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date')[:4]
			})
		else:
			messages.error(request, 'The post type is incorrect')
			return redirect('/')


postpics = ['na1.jpeg','na2.jpg','na3.jpeg','na4.jpg','na5.jpg','na6.jpg','na7.jpeg','na8.jpg','na9.jpg','na10.jpg','na11.jpg','na12.jpg','na13.jpg','na14.jpg','na15.jpg', 'na16.jpg']

def createpost(request):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else: 
		form = CreateNewPost(request.POST)
		user = User.objects.get(username=request.user.username)

		following = []
		for followMem in user.following_set.all():
			following.append(followMem.follow)

		if form.is_valid():
			newpost = Post()
			newpost.user = user
			newpost.title = form.cleaned_data['title']
			newpost.body = form.cleaned_data['body']
			newpost.postType = form.cleaned_data['postType']
			newpost.category = form.cleaned_data['category']
			newpost.background = random.choice(postpics)
			newpost.save()

			for follower in Following.objects.filter(follow=user):
				newNotification = Notification()
				newNotification.user = User.objects.get(username=follower.member)
				newNotification.message = request.user.username+' created a post on '+form.cleaned_data['postType']+'s'
				newNotification.url = '/post/'+str(newpost.pk)
				newNotification.img = 'create.png'
				newNotification.save()

				alert = newNotification.user
				alert.numofnewnote += 1;
				alert.save()

			messages.success(request, 'Post added successfully.')
			return redirect('/profile')
			# return render(request, 'index/profile.html', {
			# 	'title': request.user.username+', Welcome to your page',
			# 	'authentication': True,
			# 	'user': User.objects.get(username=request.user.username),
			# 	'following': following,
			# 	'follower_object': Following.objects.filter(follow=request.user.username)
			# })
		else:
			messages.error(request, 'Error error occured, please fill all fields')
			return render(request, 'index/profile.html', {
				'title': request.user.username+', Welcome to your page',
				'authentication': True,
				'user': User.objects.get(username=request.user.username),
				'following': following,
				'follower_object': Following.objects.filter(follow=request.user.username)
			})



def a_post(request, post_id):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else:
		""" This reture the post with id of post_id """
		user = User.objects.filter(username=request.user.username)[0]
		post = Post.objects.filter(pk=post_id)[0]
		viewed = View.objects.filter(user=user, post=post)
		if not viewed:
			newview = View(user=user, post=post)
			newview.save()

		user = User.objects.get(username=request.user.username)

		following = []
		for followMem in Following.objects.filter(member=request.user.username):
			following.append(followMem.follow.username)
		return render(request, 'post/single.html', {
			'title': post.title+' by '+post.user.username,
			'post': post,
			'authentication': True,
			'following': following,
			'user': user,
			'notification': Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date')[:4]
		})


# Editing post 
def editpost(request, post_id):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else:
		form = EditPost(request.POST)
		if form.is_valid():
			post = Post.objects.get(pk=post_id)
			post.title = form.cleaned_data['title']
			post.body = form.cleaned_data['body']
			post.postType = form.cleaned_data['postType']
			post.category = form.cleaned_data['category']
			post.edited = True
			post.save()

			for user in Postcomment.objects.filter(targetpost=post):
				newNotification = Notification()
				newNotification.user = user.author
				newNotification.message = request.user.username+' edited a post you are following'
				newNotification.url = '/post/'+str(post.pk)
				newNotification.img = 'create.png'
				newNotification.save()

				alert = user.author
				alert.numofnewnote += 1;
				alert.save()

			return redirect('/profile')
		else:
			messages.success(request, 'Update unsuccessful.')
			return redirect('/profile')

def givecomment(request, post_id):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else:
		user = User.objects.filter(username=request.user.username)[0]
		post = Post.objects.filter(pk=post_id)[0]

		viewed = View.objects.filter(user=user, post=post)
		viewed = View.objects.filter(user=user, post=post)
		
		if not viewed:
			newview = View(user=user, post=post)
			newview.save()

		form = CommentPost(request.POST)
		if form.is_valid():
			comment = Postcomment()
			comment.targetpost = post
			comment.author = User.objects.get(username=request.user.username)
			comment.body = form.cleaned_data['body']
			comment.save()

			# Ensuring the post author doesn't get a note when he give a comment
			if request.user.username != Post.objects.get(pk=post_id).user.username:
				# Creating Notification for the author of the post commented on.
				newNotification = Notification()
				newNotification.user = Post.objects.get(pk=post_id).user
				newNotification.message = request.user.username+' commented on your post named '+Post.objects.get(pk=post_id).title
				newNotification.url = '/post/'+str(post_id)
				newNotification.img = 'comment.png'
				newNotification.save()

				alert = newNotification.user
				alert.numofnewnote += 1;
				alert.save()

			# list to ensure no repetition of note to one commentator.
			givento = []
			for commentator in Postcomment.objects.filter(targetpost=Post.objects.get(pk=post_id)):
				# Ensuring the owner of post doesn't get a notification because they also commented
				if commentator.author.username != Post.objects.get(pk=post_id).user.username:
					# Ensuring the new commentator doesn't get a note if he has given a comment before.
					if request.user.username != commentator.author.username:
						
						if commentator.author.username not in givento:
							newNotification = Notification()
							newNotification.user = commentator.author
							newNotification.message = request.user.username+' gave a comment on '+Post.objects.get(pk=post_id).title+' you are following'
							newNotification.url = '/post/'+str(post_id)
							newNotification.img = 'comment.png'
							newNotification.save()

							alert = newNotification.user
							alert.numofnewnote += 1;
							alert.save()

							givento.append(commentator.author.username)

			return redirect('/profile')
		else:
			messages.success(request, 'Please the field before submitting.')
			return redirect('/profile')


def favourpost(request, post_id):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else:
		user = User.objects.filter(username=request.user.username)[0]
		post = Post.objects.filter(pk=post_id)[0]
		viewed = View.objects.filter(user=user, post=post)
		viewed = View.objects.filter(user=user, post=post)
		
		if not viewed:
			newview = View(user=user, post=post)
			newview.save()

		if Favour.objects.filter(favouredBy=user, post=post):
			messages.success(request, 'Post has been favoured before.')
		else:
			favourid = Favour(favouredBy=user, post=post)
			favourid.save()

			# Creating Notification for post being favoured
			if Post.objects.get(pk=post_id).user.username != request.user.username:
				newNotification = Notification()
				newNotification.user = Post.objects.get(pk=post_id).user
				newNotification.message = request.user.username+' favoured your post on '+Post.objects.get(pk=post_id).postType+'s'
				newNotification.url = '/post/'+str(post_id)
				newNotification.img = 'like.png'
				newNotification.save()

				alert = newNotification.user
				alert.numofnewnote += 1;
				alert.save()

			messages.success(request, 'Post added to your favourite.')

		return redirect('/profile')

def unfavourpost(request, post_id):
	if not request.user.is_authenticated:
		messages.error(request, 'Ensure you are logged in or create an account now.')
		return redirect('/sign-in')
	else:
		user = User.objects.get(username=request.user.username)
		post = Post.objects.filter(pk=post_id)
		
		if post:
			favourdetails = Favour.objects.filter(favouredBy=user, post=post[0])
			if favourdetails:
				Favour.objects.get(favouredBy=user, post=post).delete()
				messages.success(request, 'Post removed from your favourite list')
			else:
				messages.error(request, 'Post does not exit in your favourite list')

		else:
			messages.error(request, 'Post does not exit or deleted')
		

		return redirect('/profile')