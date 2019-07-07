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
		# favourites = []
		# for i in Quoteoftheday.objects.all():
		# 	favourites.push(i.pk)
		# for i in Jokeoftheday.objects.all():
		# 	favourites.push(i.pk)
		# for i in Motivationoftheday.objects.all():
		# 	favourites.push(i.pk)
		return render(request, 'index/home.html', {
			'title': 'Flick: Home page',
			'authentication': authentication,
			'user': User.objects.get(username=request.user.username),
			'Quoteoftheday': Quoteoftheday.objects.all(), 
			'Jokeoftheday': Jokeoftheday.objects.all(),
			'Motivationoftheday': Motivationoftheday.objects.all(),
			'notification': Notification.objects.filter(user=User.objects.get(username=request.user.username)).order_by('-date')[:4]
		})
	else:
		return render(request, 'index/index.html', {
			'title': 'Flick: Home page',
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
				'title': 'Flick: Contact page',
				'authentication': True,
				'user': User.objects.get(username=request.user.username),
				'notification': Notification.objects.filter(user=user).order_by('-date')[:4]
			})
		else:
			print('Not logged in')
			return render(request, 'index/contact.html', {
				'title': 'Flick: Contact page',
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
				return redirect(index)
		
		messages.error(request, 'Please ensure the all the field are filled')
		return redirect(register)
	else:
		return render(request, 'index/register.html', {'title': 'Join the moving team Flick'})

def logout(request):
	print('Logging out as', request.user)
	logout_user(request)
	return redirect(login)


def changepassword(request):
	user = User.objects.get(username=request.user.username)
	currentPassword = request.POST['currentPassword']
	password = request.POST['password']
	password2 = request.POST['newPassword2']
	if not password==password2:
		messages.error(request, 'Chosen password does not match')
		return redirect(myprofile)

	if user.check_password(currentPassword):
		user.set_password(password)
		user.save()
		messages.error(request, 'Password updated')
		return redirect(myprofile)
	else:
		messages.success(request, 'Current password given does not match, try again')
		return redirect(myprofile)


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

def isempty(word):
	word = word.strip()
	if id(word)==id(''):
		return True
	else:
		return False