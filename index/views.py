from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from .forms import UserForm, EditProfileForm, WriteOnWallForm, WallReplyForm, ContactForm,ProfilePicsForm
from index.models import User
from .models import Following, Wall, WallReply, Quoteoftheday, Jokeoftheday, Motivationoftheday
from django.contrib import messages
from .models import Oneofakind, Selectionoftheday, Likepage, Notification, Favour
from post.models import Post



# Create your views here.

def index(request):
	authentication = False
	if request.user.is_authenticated():
		authentication = True
		print('Home page session')
		# print(request.session['my_followers'])
		return render(request, 'index/home.html', {
			'title': 'Dacken: Home page',
			'authentication': authentication,
			'user': User.objects.get(username=request.user.username),
			'Quoteoftheday': Quoteoftheday.objects.all(), 
			'Jokeoftheday': Jokeoftheday.objects.all(),
			'Motivationoftheday': Motivationoftheday.objects.all(),
			'notification': Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date')[:4]
		})
	else:
		return render(request, 'index/index.html', {
			'title': 'Dacken: Home page',
			'authentication': authentication,
			'Oneofakind': Oneofakind.objects.all(),
			'Selectionoftheday': Selectionoftheday.objects.all()
		})

def notification(request):
	if not request.user.is_authenticated:
		return redirect(login)
	else:
		user = User.objects.get(username=request.user.username)
		user.numofnewnote = 0;
		user.save()
		return render(request, 'index/notification.html', {
			'title': 'Notifications',
			'authentication': True,
			'notifications': Notification.objects.filter(user=user).order_by('-date')
		})

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Message sent.')
			return redirect('/contact')
		else:
			messages.error(request, 'Please complete the query form')
			return redirect('/contact')
			
	else:
		if request.user.is_authenticated():
			user = User.objects.get(username=request.user.username)
			return render(request, 'index/contact.html', {
				'title': 'Dacken: Contact page',
				'authentication': True,
				'user': User.objects.get(username=request.user.username),
				'notification': Notification.objects.filter(user=user).order_by('-date')[:4]
			})
		else:
			print('Not logged in')
			return render(request, 'index/contact.html', {
				'title': 'Dacken: Contact page',
				'authentication': False
			})

def a_user(request, username):
	""" Allow a user view another user's profile page using the id = user_id"""
	if not request.user.is_authenticated:
		return redirect(login)
	else:
		user = User.objects.get(username=request.user.username)
		# For pushing the username of the people i am following to a list
		my_followering = []
		for followMem in Following.objects.filter(member=request.user.username):
			my_followering.append(followMem.follow.username)

		# forming the user's followers object
		his_followers = []
		for i in Following.objects.filter(follow=User.objects.get(username=username)):
			
			his_followers.append({
				'date': i.date,
				'member': User.objects.get(username=i.member)
				})



		userdetails = User.objects.get(username=username)
		return render(request, 'index/single_profile.html', {
			'title': username+' profile page',
			'loggedUser': user,
			'userdetails': userdetails,
			'posts': Post.objects.filter(user=userdetails).order_by('-date'),
			'wall': Wall.objects.filter(user=userdetails).order_by('-date'),
			'favourites': Favour.objects.filter(favouredBy=userdetails).order_by('-date'),
			'authentication': True,
			'his_followers': his_followers,
			'his_following': Following.objects.filter(member=username),
			'myfollower_object': my_followering,
			'notification': Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date')[:4]
		})


def myprofile(request):
	if not request.user.is_authenticated:
		return redirect(login)
	else:
		# print('Session')
		# print(request.session['my_followers'])
		user = User.objects.get(username=request.user.username)

		# For pushing the username of the people i am following to a list
		following = []
		for followMem in Following.objects.filter(member=request.user.username):
			following.append(followMem.follow.username)

		# Object for members following me. For my community follower's list
		follower_object = []
		for i in Following.objects.filter(follow=user):
			
			follower_object.append({
				'date': i.date,
				'member': User.objects.get(username=i.member)
				})

		return render(request, 'index/profile.html', {
			'title': request.user.username+', Welcome to your page',
			'authentication': True,
			'user': user,
			'wall': Wall.objects.filter(user=user).order_by('-date'),
			'posts': Post.objects.filter(user=user).order_by('-date'),
			'favourites': Favour.objects.filter(favouredBy=user).order_by('-date'),
			'following': following,
			'follower_object': follower_object,
			'notification': Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date')[:4],
			# this one is good to go
			'am_following': Following.objects.filter(member=request.user.username).order_by('-date')
		})


def login(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user.is_active:
				login_user(request, user)
				user = User.objects.filter(username=request.user)
				
				my_followers = []
				for followMem in User.objects.get(username=username).following_set.all():
					my_followers.append(followMem.follow)

				# request.session['my_followers'] = my_followers

				return redirect(index)
				
			else:
				messages.error(request, 'Your account has been disabled')
				return render(request, 'index/login.html', {
					'title': 'Check out the latest updates'
				})
		else:
			messages.error(request, 'Invalid login')
			return render(request, 'index/login.html', {
				'title': 'Check out the latest updates'
			})
	else:
		return render(request, 'index/login.html', {'title': 'Check out the latest updates'})


def register(request):
	if request.method=='POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)

			user.save()
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login_user(request, user)
				# user = User.objects.filter(user=request.user)
				messages.success(request, 'Registration successfull. Welcome '+username)
				return render(request, 'index/index.html', {
					'title': 'Dacken: Home page',
					'authentication': True
				})
				
		context = {
			'title': 'Join the moving team Dacken',
			'form': form,
			'error': 'Please ensure the all the field are filled'
		}
		return render(request, 'index/register.html', context)
	else:
		return render(request, 'index/register.html', {'title': 'Join the moving team Dacken'})

def logout(request):
	print('Logging out as', request.user)
	logout_user(request)
	return redirect(login)


def follow(request, username):
	follow = User.objects.get(username=username)
	if Following.objects.filter(member=request.user.username, follow=follow):
		messages.error(request, 'You have '+username+' on your following list ')
	else:
		if username == request.user.username:
			messages.error(request, "You can't follow yourself")
		else:
			fol = Following()
			fol.member = request.user.username
			fol.follow = User.objects.get(username=username)
			fol.save()

			# Creating a notification for new followship(The person being followed receive note)
			newNotification = Notification()
			newNotification.user = User.objects.get(username=username)
			newNotification.message = request.user.username+' is now following you'
			newNotification.url = '/profile/'+request.user.username
			newNotification.img = 'follow.png'

			newNotification.save()

			alert = User.objects.get(username=username)
			alert.numofnewnote += 1;
			alert.save()
			
			# request.session['my_followers'].append(username)
			# print('After following')
			# print(request.session['my_followers'])
	return redirect('/profile')

def unfollow(request, username):
	follow = User.objects.get(username=username)
	fol = Following.objects.filter(member=request.user.username, follow=follow)
	if fol:
		fol.delete()

		# Create a notification for unfollowing
		unfollowNotification = Notification()
		unfollowNotification.user = User.objects.get(username=username)
		unfollowNotification.message = request.user.username+' unfollowed you'
		unfollowNotification.url = '/profile/'+request.user.username
		unfollowNotification.img = 'follow.png'
		unfollowNotification.save()

		# alert
		alert = User.objects.get(username=username)
		alert.numofnewnote += 1;
		alert.save()


		# request.session['my_followers'].remove(username)
		# print('After Unfollowing')
		# print(request.session['my_followers'])
	else:
		print('You were not following '+username+' before')

	print('Unfollowing '+username)
	
	return redirect('/profile')

def changepassword(request):
	user = User.objects.get(username=request.user.username)
	currentPassword = request.POST['currentPassword']
	password = request.POST['password']

	if user.check_password(currentPassword):
		user.set_password(password)
		user.save()
		print('Password updated')
		return redirect('/profile')
	else:
		print('Password mismatch')
		return redirect('/profile')


IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def editprofile(request):
	form = EditProfileForm(request.POST)
	if form.is_valid():
		user = User.objects.get(username=request.user.username)
		user.first_name = form.cleaned_data['first_name']
		user.last_name = form.cleaned_data['last_name']
		user.email = form.cleaned_data['email']

		if not isempty(request.POST['aboutUser']):
			user.aboutUser = request.POST['aboutUser']
		else:
			user.aboutUser = ''

		pictureForm = ProfilePicsForm(request.POST,request.FILES)
		if pictureForm.is_valid():
			print('I think it will work')
			# pictureForm.save(commit=False)
			# pictureForm.profilePics = 

			file_type = str(request.FILES['profilePics']).split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMAGE_FILE_TYPES:
				messages.error(request, 'Image must be a jpeg, png or jpg file')
				return redirect('/profile')
			else:

				user.profilePics = request.FILES['profilePics']

				# Adding the new one
				print('He want to upload')

		user.save()

		for follower in Following.objects.filter(follow=User.objects.get(username=user.username)):
			newNotification = Notification()
			newNotification.user = User.objects.get(username=follower.member)
			newNotification.message = request.user.username+' edited her profile'
			newNotification.url = '/profile/'+request.user.username
			newNotification.img = 'profile.png'
			newNotification.save()

			# alert
			alert = User.objects.get(username=follower.member)
			alert.numofnewnote += 1;
			alert.save()

		messages.success(request ,'Your profile has been updated!')
		return redirect('/profile')
	else:
		print('Errors that occured: ')
		print(form.errors)
		return redirect('/profile')

def writeonwall(request, username):
	form = WriteOnWallForm(request.POST)
	if form.is_valid():
		if User.objects.filter(username=username):
			wall = Wall()

			wall.user = username
			wall.writer = User.objects.get(username=request.user.username)
			wall.body = form.cleaned_data['body']

			wall.save()
			
		else:
			messages.error(request, 'Invalid Username')
			return redirect('/profile')

		# Ensuring notification is not created when the wall owner writes
		if request.user.username!=username:
			# Creating Notification for new wall post
			newNotification = Notification()
			newNotification.user = User.objects.get(username=username)
			newNotification.message = request.user.username+' write on your wall'
			newNotification.url = '/profile'
			newNotification.img = 'wall.png'
			newNotification.save()

			# alert
			alert = User.objects.get(username=username)
			alert.numofnewnote += 1;
			alert.save()
		else:
			for follower in Following.objects.filter(follow=User.objects.get(username=request.user.username)):

				newNotification = Notification()
				newNotification.user = User.objects.get(username=follower.member)
				newNotification.message = follower.follow.username+' write her wall'
				newNotification.url = '/profile/'+follower.follow.username
				newNotification.img = 'wall.png'
				newNotification.save()

				# alert
				alert = User.objects.get(username=follower.member)
				alert.numofnewnote += 1;
				alert.save()


		messages.success(request, 'Write-up posted on wall')
		return redirect('/profile')
	else:
		print('Error occured!')
		print(form.errors)
		return redirect('/profile')

def writewallreply(request, wall_id):
	form = WallReplyForm(request.POST)
	if form.is_valid():
		wallreply = WallReply()
		wallreply.wall = Wall.objects.get(pk=wall_id)
		wallreply.body = form.cleaned_data['body']
		wallreply.writer = User.objects.get(username=request.user.username)

		wallreply.save()
		
		# Creating Notification for owner of the write up
		print('Writers name')
		print(wallreply.writer.username)

		if Wall.objects.get(pk=wall_id).user != wallreply.writer.username:
			print('In for businness')
			ownerNote = Notification()
			ownerNote.user = wallreply.writer
			ownerNote.message = request.user.username+' reply on your write up on '+Wall.objects.get(pk=wall_id).user+' wall'
			ownerNote.url = '/profile/'+ Wall.objects.get(pk=wall_id).user
			ownerNote.img = 'wall.png'
			ownerNote.save()

			# alert
			alert = wallreply.writer
			alert.numofnewnote += 1;
			alert.save()

			wallerNote = Notification()
			wallerNote.user = User.objects.get(username=Wall.objects.get(pk=wall_id).user)
			wallerNote.message = request.user.username+' reply on a write up on your wall'
			wallerNote.url = '/profile'
			wallerNote.img = 'wall.png'
			wallerNote.save()

			# alert
			alert = wallerNote.user;
			alert.numofnewnote += 1;
			alert.save()



		return redirect('/profile')
	else:
		print('Error occured parsing wallreply')
		print(form.errors)
		return redirect('/profile')

def likepage(request, username):
	if request.user.username == username:
		# This is to ensure a user can't like his/her own page
		messages.error(request, "Sorry, you can't like you own page ")
		return redirect('/profile')
	else:
		user = User.objects.filter(username=username)[0]
		exitence = Likepage.objects.filter(user=user, fan=request.user.username)

		# The above decision is to ensure you can't a page more than once.
		if exitence:
			messages.error(request, 'You have liked this page before')
			return redirect('/profile')
		else:
			
			if user:
				likepage = Likepage(user=user, fan=request.user.username)
				likepage.save()
				messages.success(request, "You liked "+username+"'s page ")

				# Creating Notification for new page liking
				newNotification = Notification()
				newNotification.user = user
				newNotification.message = request.user.username+' like your page'
				newNotification.url = '/profile/'+request.user.username
				newNotification.img = 'home.png'
				newNotification.save()

				# alert
				alert = user
				alert.numofnewnote += 1;
				alert.save()

				return redirect('/profile')
			else:
				messages.error(request, 'The member you want to follow is invalid.')
				return redirect('/profile')

	
def checknotification(request):
	# print('Hello, this checknotification')
	if not request.user.is_authenticated:
		return redirect(login)
	else:
		disharm = User.objects.get(username=request.user.username)
		disharm.numofnewnote = 0;
		disharm.save()

		return None;

def isempty(word):
	word = word.strip()
	if id(word)==id(''):
		return True
	else:
		return False