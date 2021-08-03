from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from . import models
from authentication import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template import loader


# ====================================================methods==============================================================
def split(queryset, n):
    q, r = divmod(len(queryset), n)
    return (queryset[i*q+min(i, r):(i+1)*q+min(i+1, r)] for i in range(n))

def lazy_load(page, model, results_per_page):
    objects = model.objects.all()
    paginator = Paginator(objects, results_per_page)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(2)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    splitted_objects = split(objects, 3)
    objects_html = loader.render_to_string(
        'lazy_load_template.html',
        {'objects':splitted_objects}
    )
    return JsonResponse(
        {
            'objects_html':objects_html,
            'has_next':objects.has_next()
        }
    )
# =========================================================================================================================



    


def home(request, page=None):
    if page is None:
        users = models.BlogUser.objects.all()[:10]
        posts = models.Post.objects.filter(is_draft=False)[:8]
        data = split(posts, 2) if posts else None
        return render(request, 'home.html', {'users': users, 'posts': data})
    else:
        return lazy_load(page, models.Post, 10)


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

    data = split(posts, 3) if posts else None
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
            return redirect('user')
    return redirect('write')
