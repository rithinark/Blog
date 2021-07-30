from django.http.response import Http404
from rest_framework.response import Response
from . import models
from .import serializers
from .permissions import IsGetOrIsAuthenticated
from rest_framework.views import APIView
from rest_framework import permissions, viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser




class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


# class TagViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     queryset = models.Tag.objects.all()
#     serializer_class = serializers.TagSerializer


class VoteList(APIView):

    def post(self, request, formate=None):
        request.data["user"] = request.user.id
        serializer = serializers.VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteDetail(APIView):

    permission_classes = [IsGetOrIsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, user_id, post_id):
        try:
            return models.Vote.objects.filter(post=post_id, user=user_id).first()
        except models.Vote.DoesNotExist:
            raise Http404

    def get(self, request, post_id, format=None):
        vote = self.get_object(request.user.id, post_id)
        serializer = serializers.VoteSerializer(vote)
        uvotes = models.Vote.objects.filter(
            post=post_id, vote='UPVOTE').count()
        dvotes = models.Vote.objects.filter(
            post=post_id, vote='DOWNVOTE').count()
        data = {'votes_count': uvotes-dvotes}
        data.update(serializer.data)
        return Response(data)

    def put(self, request, post_id, format=None):
        vote = self.get_object(request.user.id, post_id)
        serializer = serializers.VoteSerializer(
            vote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        vote = self.get_object(request.user.id, post_id)
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewList(APIView):

    def post(self, request, post_id, format=None):
        request.data["user"] = request.user.id
        review = models.Review.objects.filter(
            user=request.user.id, post=post_id)
        if review:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPictureDetails(APIView):
    permission_classes = [IsGetOrIsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

        
    def put(self, request, format=None):
        user_detail = models.UserDetail.objects.filter(user=request.user).first()
        serializer = serializers.BlogUserDetailSerializer(user_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

        
      

         


class FollowView(APIView):
    pass
