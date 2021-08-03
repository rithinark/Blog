from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from . import forms
from . import models
from .image_processing import Image_processing
# Create your views here.

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
    return render(request, 'auth/login.html', {'form': form})


def regist(request):
    if request.POST:
        form = forms.RegistForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')
            user = authenticate(username=email, password=password)
            user_detail = models.UserDetail.objects.create(user=user, about="Hi there, I am a Blogger",
            profile_img=Image_processing.createDefaultProfile(user))
            user_detail.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = forms.RegistForm()

    return render(request, 'auth/regist.html', {"form": form})


def logout(request):
    auth_logout(request=request)
    return redirect('home')

