from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render , redirect
from . import forms
# Create your views here.


def home(request):
    return render(request, 'home.html')


def post(request):
    return render(request, 'post.html')


def user(request):
    return render(request, 'user.html')



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




def create_post(request):

    return render (request, 'createpost.html')