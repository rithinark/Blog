from django.urls import path
from . import views;
urlpatterns = [
    #auth
    path('login', views.login, name='login'),
    path('regist', views.regist),

    #crud
    path('create', views.create_post),

    path('', views.home, name='home'),
    path('post', views.post,),
    path('user', views.user),

    
]
