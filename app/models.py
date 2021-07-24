from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class BlogUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class BlogUser(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_username(self):
        return self.username

    def __str__(self):
        return self.email

    objects = BlogUserManager()


class UserDetail(models.Model):
    about = models.CharField(max_length=1000)
    profile_img = models.ImageField(upload_to='images/profiles')


class Tag(models.Model):
    tags = models.CharField(max_length=16)


class Post(models.Model):
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=32)
    content = models.TextField()
    published_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tumbnail = models.ImageField(upload_to='images/posts')


class Review(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    vote = models.IntegerField(
        choices=(
            ('UPVOTE', 'upvote'),
            ('DOWNVOTE', 'downvote')
        )
    )


class Follower(models.Model):
    user = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, related_name='follower')
    followed_on = models.DateTimeField()


class BookMark(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
