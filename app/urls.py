from django.urls import path, include, re_path
from . import views
from . import api
from rest_framework.routers import DefaultRouter
from rest_framework import routers

router = DefaultRouter()
router.register(r'posts', api.PostViewSet, basename='post')
router.register(r'tag', api.TagViewSet)



urlpatterns = [
    #auth
    path('login', views.login, name='login'),
    path('regist', views.regist, name="sign up"),
    path('logout', views.logout, name="logout"),

    #pages
    path('write/', views.create_post, name='write'),
    path('write/<int:post_id>/', views.create_post),
    path('publish/<int:post_id>', views.publish),

    path('', views.home, name='home'),
    path('post', views.post,name="post"),
    path('user', views.user, name="profile"),

    #api
    path(r'api/', include(router.urls)),
    path('post-write', api.PostWrite.as_view())

    
]
