from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .image_processing import Image_processing
from . import forms
from . import models
# Create your views here.

# ===================================================auth views============================================================


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
            profile_img=Image_processing.createDefaultProfile(user.email))
            user_detail.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = forms.RegistForm()

    return render(request, 'auth/regist.html', {"form": form})


def logout(request):
    auth_logout(request=request)
    return redirect('home')


# =======================================================page views=========================================================
def home(request):
    users = models.BlogUser.objects.all()[:5]
    posts = models.Post.objects.filter(is_draft=False)[:5]

    data = [[], [], []]
    counter = 0
    for post in posts:
        if counter == 2:
            counter = 0
        data[counter].append(post)
        counter += 1
    return render(request, 'home.html', {'users': users, 'posts': data})


def post(request, post_id):
    post = get_object_or_404(models.Post, id=post_id)
    comments = models.Review.objects.filter(post=post_id)

    return render(request, 'post.html', {'post': post, 'comments': comments})


def user(request, user_id=None):

    if user_id:
        user = get_object_or_404(models.BlogUser, id=user_id)
    else:
        user = request.user if request.user.is_authenticated else Http404
    try:
        user_details = user.userdetail
    except models.UserDetail.DoesNotExist:
        user_details = None
    posts = models.Post.objects.filter(
        author=user.id).exclude(is_draft=True)

    data = [[], [], []]
    counter = 0
    for post in posts:
        if counter == 3:
            counter = 0
        data[counter].append(post)
        counter += 1
    context = {
        'userP': user,
        'user_details': user_details,
        'posts': data,
        'post_count': len(posts),
    }
    return render(request, 'user.html', context)


def profileEdit(request):
    if request.method == 'POST':
        form = forms.ProfileEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user')
    else:
        form = forms.ProfileEditForm()
    return render(request, 'profile-edit.html', {'form': form})


def create_post(request, post_id=None):
    if request.user.is_authenticated:
        if post_id is None:
            try:
                drafted_post = models.Post.objects.get(
                    author=request.user, is_draft=True)
            except models.Post.DoesNotExist:
                drafted_post = None
            if drafted_post:
                return redirect(f'/write/{drafted_post.id}')
            new_post = models.Post(author=request.user, is_draft=True)
            new_post.save()
            return redirect(f'/write/{new_post.id}')

        drafted_post = get_object_or_404(
            models.Post, author=request.user, id=post_id)
        return render(request, 'createpost.html', {'post': drafted_post})
    raise Http404


def publish(request, post_id):
    if post_id:
        post = models.Post.objects.get(id=post_id)
        if post and post.publish():
            return redirect('profile')
    return redirect('write')
