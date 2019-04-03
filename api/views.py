from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from index.models import Wall, User, Following
from .serializers import WallSerializer, FollowingSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# def index(request):
# 	return render(request, 'video/index.html', {
# 		'title': 'List of video names'
# 	})

class WallList(APIView):

	def get(self, request):
		objs = Wall.objects.all()
		serializer = WallSerializer(objs, many=True)
		return Response(serializer.data)

	permission_classes = ( IsAuthenticated, )
	def post(self, request):
		data = {
			'body': request.data['body'],
			'user': request.data['user'],
			'writer': User.objects.get(username=request.user.username).pk
		}
		serializer = WallSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			print('Post request was successful!')
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			print('Server: Sorry, please fill all the form!')
			return redirect('/profile')
		return redirect('/profile')

class Following(APIView):
	def get(self, request):
		following = []
		for followMem in Following.objects.filter(member=request.user.username):
			following.append(followMem.follow.username)
		print('Following!')
		print(following)

		serializer = FollowingSerializer(following, many=True)
		print('Serialized data')
		print(serializer.data)
		return Response(serializer.data)