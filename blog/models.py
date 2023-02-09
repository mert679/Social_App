from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    followers = models.ManyToManyField("Follow",blank=True,related_name="follow_user")

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.CharField(max_length=500,null=True,blank=True)
    timestamp = models.DateField(auto_now_add=True)
    like = models.ManyToManyField(User,blank=True,related_name="liked_user")
    
    @property
    def number_of_likes(self):
        return self.like.all().count(),
    def __str__(self) -> str:
        return self.post



class Follow(models.Model):
    followed_me = models.ForeignKey(User, on_delete=models.CASCADE,related_name="followed_me", default=None)
    followed_by  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_by", default=None)

    def __str__(self) -> str:
        return f"{self.followed_by.username} start following {self.followed_me.username} "