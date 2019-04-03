from rest_framework import serializers
from index.models import Wall, Following

class WallSerializer(serializers.ModelSerializer):
	class Meta:
		model = Wall
		fields = '__all__' 

class FollowingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Following
		fields = '__all__'