from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def post(request):
    return render(request, 'post.html')


def user(request):
    return render(request, 'user.html')


def login(request):
    return render(request, 'auth/login.html')

def regist(request):
    return render(request, 'auth/regist.html')
