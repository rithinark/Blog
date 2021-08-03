from django.db import models
from django.utils import timezone
from authentication.models import BlogUser
# Create your models here.



class Post(models.Model):
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=40, null=True)
    content = models.TextField(null=True)
    published_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tumbnail = models.ImageField(upload_to='images/posts', null=True)
    is_draft = models.BooleanField(default=True)

    def publish(self, *args, **kwargs):
        if not (self.content and self.tumbnail):
            return False
        self.is_draft = False
        self.published_at = timezone.now()
        super(Post, self).save(*args, **kwargs)
        return True
    
    def getVotes(self):
        uvotes = Vote.objects.filter(
            post=self.id, vote='UPVOTE').count()
        dvotes = Vote.objects.filter(
            post=self.id, vote='DOWNVOTE').count()
        return uvotes-dvotes


class Review(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    vote = models.CharField(
        choices=(
            ('UPVOTE', 'upvote'),
            ('DOWNVOTE', 'downvote')
        ),
        max_length=8,
    )



#===========================================need to include=================================================================
# class Follower(models.Model):
#     user = models.ForeignKey(
#         BlogUser, on_delete=models.CASCADE, related_name='user')
#     follower = models.ForeignKey(
#         BlogUser, on_delete=models.CASCADE, related_name='follower')
#     followed_on = models.DateTimeField()
# class Tag(models.Model):
#     tags = models.CharField(max_length=16, unique=True)


# class BookMark(models.Model):
#     user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
