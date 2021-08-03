from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
# router.register(r'tag', api.TagViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'votes/', views.VoteList.as_view()),
    path(r'vote/<int:post_id>/', views.VoteDetail.as_view()),
    path(r'reviews/<int:post_id>/', views.ReviewList.as_view()),
    path(r'userdetails/', views.UserPictureDetails.as_view())
]
