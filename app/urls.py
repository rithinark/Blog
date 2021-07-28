from django.urls import path, include, re_path
from . import views
from . import api
from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = DefaultRouter()
router.register(r'posts', api.PostViewSet, basename='post')
router.register(r'tag', api.TagViewSet)
router.register(r'userdetails', api.BlogUserDetails)




urlpatterns = [
    #auth
    path('login', views.login, name='login'),
    path('regist', views.regist, name="sign up"),
    path('logout', views.logout, name="logout"),

    #pages
    path('write/', views.create_post, name='write'),
    path('write/<int:post_id>/', views.create_post),
    path('publish/<int:post_id>', views.publish),
    path('post/<int:post_id>', views.post),

    path('', views.home, name='home'),

    path('user', views.user, name="profile"),
    path('profile-edit', views.profileEdit),

    #api
    path(r'api/', include(router.urls)),
    path(r'api/votes/', api.VoteList.as_view()),
    path(r'api/vote/<int:post_id>/', api.VoteDetail.as_view())
    

    
]
