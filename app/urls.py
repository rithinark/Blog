from django.urls import path, include
from . import views
from . import api
from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = DefaultRouter()
router.register(r'posts', api.PostViewSet, basename='post')
# router.register(r'tag', api.TagViewSet)



urlpatterns = [
    # auth
    path('login', views.login, name='login'),
    path('regist', views.regist, name="sign up"),
    path('logout', views.logout, name="logout"),

    # pages
    path('', views.home, name='home'),

    path('write/', views.create_post, name='write'),
    path('write/<int:post_id>/', views.create_post),
    path('publish/<int:post_id>', views.publish),
    path('post/<int:post_id>', views.post),

    path('user', views.user, name="profile"),
    path('user/<int:user_id>', views.user, name="profile"),
    path('profile-edit', views.profileEdit),

    # api
    path(r'api/', include(router.urls)),
    path(r'api/votes/', api.VoteList.as_view()),
    path(r'api/vote/<int:post_id>/', api.VoteDetail.as_view()),
    path(r'api/reviews/<int:post_id>/',api.ReviewList.as_view()),
    path(r'api/userdetails/',api.UserPictureDetails.as_view())

]
