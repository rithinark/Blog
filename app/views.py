from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render , redirect, get_object_or_404
from django.http import Http404
from . import forms
from . import models
# Create your views here.

#===================================================auth views============================================================
def login(request):
    if request.POST:
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    else:
        form = forms.LoginForm()
    return render(request, 'auth/login.html',{'form':form})

def regist(request):
    if request.POST:
        form = forms.RegistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.RegistForm()

    return render(request, 'auth/regist.html', {"form":form})


def logout(request):
    auth_logout(request=request)
    return redirect('home')



#=======================================================page views=========================================================
def home(request):
    return render(request, 'home.html')


def post(request):
    return render(request, 'post.html')


def user(request):
    return render(request, 'user.html')
    
def create_post(request,post_id=None):
    if post_id is None:
        if request.user.is_authenticated:
            try:
                drafted_post = models.Post.objects.get(author=request.user, is_draft=True)
            except models.Post.DoesNotExist:
                drafted_post = None
            if drafted_post:
                return redirect(f'/write/{drafted_post.id}')
            new_post = models.Post(author=request.user, is_draft=True)
            new_post.save()
            return redirect(f'/write/{new_post.id}')
        raise Http404
    
    drafted_post = get_object_or_404(models.Post, author=request.user, id=post_id)
    return render (request, 'createpost.html',{'post':drafted_post})

def publish(request, post_id):
    if post_id:
        post = models.Post.objects.get(id=post_id)
        if post and post.publish():
            return redirect('profile')
    return redirect('write')
    



