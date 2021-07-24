from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# Create your models here.


class BlogUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class BlogUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    def get_username(self):
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

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
    content = models.TextField(null=True)
    published_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tumbnail = models.ImageField(upload_to='images/posts', null=True)

    def publish(self, *args, **kwargs):
        if self.content and self.tumbnail:
            self.published_at = timezone.now()
        return super(Post, self).save(*args, **kwargs)




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
