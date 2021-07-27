from rest_framework.response import Response
from . import models
from .import serializers
from rest_framework.views import APIView
from rest_framework import permissions, viewsets,status
from rest_framework.parsers import MultiPartParser, FormParser



class PostWrite(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]






class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


 


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer