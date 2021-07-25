from rest_framework.response import Response
from . import models
from .import serializers
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import authentication, permissions

class PostWrite(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        usernames = [user.fullname for user in models.BlogUser.objects.all()]
        return Response(usernames)


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


 


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer