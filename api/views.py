from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from post.models import Post, Postcomment
from index.models import Contact, Wall, Likepage, User, Following, Notification, View, Favour
from .serializers import ContactMsgSerializer, PostCommentSerializer, AddPostSerializer, PostSerializer, WallSerializer, WallReplySerializer, FollowingSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
import random


class WallList(APIView):

	permission_classes = (IsAuthenticated,)

	# Logged in user writing on his wall
	def post(self, request):
		serializer = WallSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			# Ensuring notification is not created when the wall owner writes
			username = request.data['user'] # username of the user(wall owner)

			if not request.user.username==username:
				# Creating Notification for new wall post
				newNotification = Notification(user=User.objects.get(username=username), img='wall.png', url='/profile', message=request.data['writer']+' write on your wall') 
				newNotification.save()

				# alert
				alert = newNotification.user
				alert.numofnewnote += 1;
				alert.save()
			else:

				for follower in Following.objects.filter(follow=User.objects.get(username=username)):

					newNotification = Notification(user=User.objects.get(username=follower.member), message=follower.follow.username+' write their wall', url='/profile/'+follower.follow.username, img='wall.png')
					newNotification.save()

					# alert
					alert = User.objects.get(username=follower.member)
					alert.numofnewnote += 1;
					alert.save()

			writer = User.objects.get(pk=serializer.data['writer'])

			newData = serializer.data
			newData['username'] = writer.username

			if not writer.profilePics:
				newData['profilePics'] = '/static/index/media/default.png'
			else:
				newData['profilePics'] = writer.profilePics.url

			print('New wall data')
			print(newData)
			return Response(newData, status=status.HTTP_201_CREATED)
		
		return Response(False)


class ReplyWallpost(APIView):
	permission_classes = (IsAuthenticated,)

	# Logged in user replying on his wall
	def post(self, request):
		serializer = WallReplySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			newData = serializer.data
			
			# Creating Notification for owner of the write up
			wallOwner = Wall.objects.get(pk=newData['wall']).user
			if wallOwner != User.objects.get(pk=newData['writer']).username:
				ownerNote = Notification(user=Wall.objects.get(pk=newData['wall']).writer, message=request.user.username+' reply on your write up on '+wallOwner+' wall', url='/profile/'+ wallOwner, img='wall.png')
				ownerNote.save()

				# alert for the wall writer
				alert = ownerNote.user
				alert.numofnewnote += 1;
				alert.save()

				wallerNote = Notification(user=User.objects.get(username=wallOwner),message=request.user.username+' reply on a write up on your wall', url='/profile', img='wall.png')
				wallerNote.save()

				# alert for the wall owner
				alert = wallerNote.user;
				alert.numofnewnote += 1;
				alert.save()


			# getting the profilePics of the writer
			writer = User.objects.get(pk=newData['writer'])
			if not writer.profilePics:
				newData['profilePics'] = '/static/index/media/default.png'
			else:
				newData['profilePics'] = writer.profilePics.url

			newData['writer'] = writer.username
			newData['replybody'] = newData['body']
			del newData['body']

			print('Wall reply')
			print(newData)
			return Response(newData, status=status.HTTP_201_CREATED)
		
		return Response(False)


class FollowingApi(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request, action, username):
		if action=='follow':
			if Following.objects.filter(member=request.user.username, follow=User.objects.get(username=username)):
				return Response(True)
			else:
				if username == request.user.username:
					return Response(False)
				else:
					fol = Following(member=request.user.username,follow=User.objects.get(username=username))
					fol.save()

					# Creating a notification for new followship(The person being followed receive note)
					newNotification = Notification(user=User.objects.get(username=username),message=request.user.username+' is now following you',url='/profile/'+request.user.username,img='follow.png')
					newNotification.save()

					alert = newNotification.user
					alert.numofnewnote += 1;
					alert.save()

					return Response(User.objects.get(username=username).profilePics.url)
		elif action=='unfollow':
			fol = Following.objects.filter(member=request.user.username, follow=User.objects.get(username=username))
			if fol:
				fol.delete()

				# Create a notification for unfollowing
				unfollowNote = Notification(user=User.objects.get(username=username),message=request.user.username+' unfollowed you',url='/profile/'+request.user.username,img='follow.png') 
				unfollowNote.save()

				# alert
				alert = unfollowNote.user
				alert.numofnewnote += 1;
				alert.save()
				return Response(True)
			else:
				return Response(False)
		else:
			return Response(False)

class FavourPost(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request, action, post_id):
		if not Post.objects.filter(pk=post_id): # Checking if the post exist
			return False;

		post = Post.objects.get(pk=post_id)
		if action=='favour':
			print('Favour')
			user = User.objects.get(username=request.user.username)
			viewed = View.objects.filter(user=user, post=post)
			
			if not viewed:
				newview = View(user=user, post=post)
				newview.save()

			if Favour.objects.filter(favouredBy=user, post=post):
				return Response(False)
			else:
				favourid = Favour(favouredBy=user, post=post)
				favourid.save()

				# Creating Notification for post being favoured
				if Post.objects.get(pk=post_id).user.username != request.user.username:
					newNote = Notification(user=Post.objects.get(pk=post_id).user,message=user.username+' favoured your post on '+Post.objects.get(pk=post_id).postType,url='/post/'+str(post_id),img='like.png')
					newNote.save()

					alert = newNote.user
					alert.numofnewnote += 1;
					alert.save()

				return Response(True)
		elif action=='unfavour':
			print('Unfavour')
			user = User.objects.get(username=request.user.username)			
			if Favour.objects.filter(favouredBy=user, post=post):
				Favour.objects.get(favouredBy=user, post=post).delete()
				return Response(True)
			else:
				return Response(False)
		else:
			return Response(False)

class Editpost(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request, post_id):
		if not Post.objects.filter(pk=post_id):
			return Response(False)

		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			post = Post.objects.get(pk=post_id)
			post.title = serializer.data['title']
			post.body = serializer.data['body']
			post.postType = serializer.data['postType']
			post.category = serializer.data['category']
			post.edited = True
			post.save()

			for user in Postcomment.objects.filter(targetpost=post):
				newNote = Notification(user=user.author,message=request.user.username+' edited a post you are following',url='/post/'+str(post.pk),img='create.png')
				newNote.save()

				alert = user.author
				alert.numofnewnote += 1;
				alert.save()

			return Response(serializer.data)
		else:
			return Response(False)

postpics = ['na1.jpeg','na2.jpg','na3.jpeg','na4.jpg','na5.jpg','na6.jpg','na7.jpeg','na8.jpg','na9.jpg','na10.jpg','na11.jpg','na12.jpg','na13.jpg','na14.jpg','na15.jpg', 'na16.jpg']

class Addpost(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		serializer = AddPostSerializer(data=request.data)
		if serializer.is_valid():
			# logged in user
			user = User.objects.get(username=request.user.username)
			serializer.save()
			newData = serializer.data

			post = Post.objects.get(pk=serializer.data['id'])
			newData['background'] = post.background = random.choice(postpics)
			post.save()
			newData['date'] = post.date

			following = []
			for followMem in user.following_set.all():
				following.append(followMem.follow)


			for follower in Following.objects.filter(follow=user):
				newNote = Notification(user=User.objects.get(username=follower.member),message=user.username+' created a post on '+serializer.data['postType']+'s',url='/post/'+str(serializer.data['id']),img='create.png')
				newNote.save()

				alert = newNote.user
				alert.numofnewnote += 1;
				alert.save()

			return Response(newData)
		else:
			print(serializer.errors)
			return Response(False)

class Commentpost(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		serializer = PostCommentSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			post_id = serializer.data['targetpost']
			user = User.objects.get(username=request.user.username)
			post = Post.objects.get(pk=post_id)
			post_date = post.date

			viewed = View.objects.filter(user=user, post=post)
			
			if not viewed:
				newview = View(user=user, post=post)
				newview.save()

			
			# Ensuring the post author doesn't get a note when he give a comment
			if request.user.username != Post.objects.get(pk=post_id).user.username:
				# Creating Notification for the author of the post commented on.
				newNote = Notification(user=Post.objects.get(pk=post_id).user,message=request.user.username+' commented on your post named '+Post.objects.get(pk=post_id).title,url='/post/'+str(post_id),img='comment.png')
				newNote.save()

				alert = newNote.user
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
							newNotification = Notification(user=commentator.author,message=request.user.username+' gave a comment on '+Post.objects.get(pk=post_id).title+' you are following',url='/post/'+str(post_id),img='comment.png')
							newNotification.save()

							alert = newNotification.user
							alert.numofnewnote += 1;
							alert.save()

							givento.append(commentator.author.username)

			newData = serializer.data
			authorObj = User.objects.get(pk=newData['author'])
			newData['author'] = authorObj.username
			if authorObj.profilePics:
				newData['profilePic'] = authorObj.profilePics.url
			else:
				newData['profilePic'] = '/static/index/media/default.png'

			newData['comDate'] = post_date
			newData['comBody'] = newData['body']
			del newData['body']

			print('Post comment new data')
			print(newData)
			return Response(newData)

		else:
			print(serializer.errors)
			return Response(False)

class LikePage(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request, username):
		if not User.objects.filter(username=username):
			return Response('The member you want to follow is invalid.')
		if request.user.username == username:
			# This is to ensure a user can't like his/her own page
			return Response("Sorry, you can't like you own page ")
		else:
			user = User.objects.get(username=username)
			exitence = Likepage.objects.filter(user=user, fan=request.user.username)

			# The above decision is to ensure you can't a page more than once.
			if exitence:
				return Response('You have liked this page before')
			else:
				likepage = Likepage(user=user, fan=request.user.username)
				likepage.save()

				# Creating Notification for new page liking
				newNote = Notification(user=user,message=request.user.username+' like your page',url='/profile/'+request.user.username, img='home.png')
				newNote.save()

				# alert
				alert = newNote.user
				alert.numofnewnote += 1;
				alert.save()

				return Response("You liked "+username+"'s page")
				
class Checknotification(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		disharm = User.objects.get(username=request.user.username)
		disharm.numofnewnote = 0;
		disharm.save()

		return Response(True);

class Contact(APIView):
	def post(self, request):
		serializer = ContactMsgSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response('Thanks for getting in touch. Message has been sent')
		else:
			return Response(False)

class SearchUsername(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		username = request.data['username'].replace(' ', '')
		if not username:
			return Response(False)

		searchResult = User.objects.filter(username__icontains=username)
		if not searchResult:
			return Response(False)

		finalResult = []
		eachResult = {}
		for i in searchResult:
			eachResult['username'] = i.username
			if i.profilePics:
				eachResult['profilePics'] = i.profilePics.url
			else:
				eachResult['profilePics'] = '/static/index/media/default.png'
			eachResult['noOfPost'] = i.post_set.count()

			finalResult.append(eachResult)
			eachResult = {}


		return Response(finalResult)

class SearchPost(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		title = request.data['title'].replace(' ', '')
		if not title:
			print('Empty')
			return Response(False)

		searchResult = Post.objects.filter(title__icontains=title)
		if not searchResult:
			print('No found')
			return Response(False)

		finalResult = []
		eachResult = {}
		for i in searchResult:
			eachResult['id'] = i.pk
			eachResult['author'] = i.user.username
			eachResult['background'] = i.background
			eachResult['title'] = i.title

			finalResult.append(eachResult)
			eachResult = {}

		print('Post search result')
		print(finalResult)
		return Response(finalResult)

