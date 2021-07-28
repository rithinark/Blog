from rest_framework import serializers
from . import models


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BlogUser
        fields =('email', 'password')

class BlogUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDetail
        fields= '__all__'

        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields='__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields =('id','tags','content', 'title','author','tumbnail')
        read_only_fields=['author']
        extra_kwargs = {'tags':{'required':False}}

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields= '__all__'




