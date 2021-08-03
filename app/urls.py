from django.urls import path
from . import views

urlpatterns = [
    # pages
    path('', views.home, name='home'),
    path('posts/<int:page>/', views.home),

    path('write/', views.create_post, name='write'),
    path('write/<int:post_id>/', views.create_post),
    path('publish/<int:post_id>/', views.publish),
    path('post/<int:post_id>/', views.post, name='post'),

    path('user/', views.user, name="user"),
    path('user/<int:user_id>/', views.user, name="profile"),
    path('profile-edit/', views.profileEdit),
]
