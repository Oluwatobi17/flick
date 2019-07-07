from django.shortcuts import render, redirect
from post.models import Post, Postcomment
from .forms import EditPost, CommentPost, CreateNewPost
from index.models import User, Favour, Following, View, Notification
from django.contrib import messages

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

# def givecomment(request, post_id):
# 	if not request.user.is_authenticated:
# 		messages.error(request, 'Ensure you are logged in or create an account now.')
# 		return redirect('/sign-in')
# 	else:
# 		user = User.objects.filter(username=request.user.username)[0]
# 		post = Post.objects.filter(pk=post_id)[0]

# 		viewed = View.objects.filter(user=user, post=post)
# 		viewed = View.objects.filter(user=user, post=post)
		
# 		if not viewed:
# 			newview = View(user=user, post=post)
# 			newview.save()

# 		form = CommentPost(request.POST)
# 		if form.is_valid():
# 			comment = Postcomment()
# 			comment.targetpost = post
# 			comment.author = User.objects.get(username=request.user.username)
# 			comment.body = form.cleaned_data['body']
# 			comment.save()

# 			# Ensuring the post author doesn't get a note when he give a comment
# 			if request.user.username != Post.objects.get(pk=post_id).user.username:
# 				# Creating Notification for the author of the post commented on.
# 				newNotification = Notification()
# 				newNotification.user = Post.objects.get(pk=post_id).user
# 				newNotification.message = request.user.username+' commented on your post named '+Post.objects.get(pk=post_id).title
# 				newNotification.url = '/post/'+str(post_id)
# 				newNotification.img = 'comment.png'
# 				newNotification.save()

# 				alert = newNotification.user
# 				alert.numofnewnote += 1;
# 				alert.save()

# 			# list to ensure no repetition of note to one commentator.
# 			givento = []
# 			for commentator in Postcomment.objects.filter(targetpost=Post.objects.get(pk=post_id)):
# 				# Ensuring the owner of post doesn't get a notification because they also commented
# 				if commentator.author.username != Post.objects.get(pk=post_id).user.username:
# 					# Ensuring the new commentator doesn't get a note if he has given a comment before.
# 					if request.user.username != commentator.author.username:
						
# 						if commentator.author.username not in givento:
# 							newNotification = Notification()
# 							newNotification.user = commentator.author
# 							newNotification.message = request.user.username+' gave a comment on '+Post.objects.get(pk=post_id).title+' you are following'
# 							newNotification.url = '/post/'+str(post_id)
# 							newNotification.img = 'comment.png'
# 							newNotification.save()

# 							alert = newNotification.user
# 							alert.numofnewnote += 1;
# 							alert.save()

# 							givento.append(commentator.author.username)

# 			return redirect('/profile')
# 		else:
# 			messages.success(request, 'Please the field before submitting.')
# 			return redirect('/profile')
