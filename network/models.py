from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 

class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="posted by", related_name="posts")
    text = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="posted on")
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')


    # Model naming
    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"Post {self.id} made by {self.user} on {self.date.strftime('%d %b %Y %H:%M:%S')}"

    def likes_int(self):
        return self.liked.all().count()

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Following(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers" )

    class Meta:
        verbose_name = "following"
        verbose_name_plural = "followings"
        unique_together = ['user', 'user_followed']

    def __str__(self):
        return f"{self.user} is following {self.user_followed}"

    def get_user_followed_posts(self):
        """ Get all the posts from users that the current user follows """

        return self.user_followed.posts.order_by("-date").all()


class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.post)