from rest_framework import serializers
from authentication import models as authmodels
from app import models


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = authmodels.BlogUser
        fields = ('email', 'password')


class BlogUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = authmodels.UserDetail
        fields = '__all__'


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Tag
#         fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('id', 'content', 'title', 'author', 'tumbnail')
        read_only_fields = ['author']
        # extra_kwargs = {'tags': {'required': False}}


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vote
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']