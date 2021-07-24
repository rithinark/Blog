from django.urls import path
from . import views;
urlpatterns = [
    #auth
    path('login', views.login),
    path('regist', views.regist),


    path('', views.home),
    path('post', views.post),
    path('user', views.user),

    
]
