from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,Http404
from django.core.paginator import Paginator
import json


# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request,"blog/register.html",{
                "message":"Password must match"
            })

        try:
            user = User.objects.create_user(username,email,password)
            user.save()

        except IntegrityError:
            return render(request,"blog/register.html",{
                "message": "Username already taken."
            })


    return render(request,"blog/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        psw = request.POST["password"]

        user = authenticate(request,username=username,password=psw)

        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render( request,"blog/login.html",{
                "message":"Invalid username and/or password."
            })

    return render(request, "blog/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def addPost(request):

    if request.method == "POST":
        body = request.POST["body"]
        post = Post(user= request.user, post = body)
        post.save()
        return redirect("index")
    return render(request,"blog/addpost.html")



def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    page = request.GET.get('page',1)
    paginator = Paginator(posts,3)

    part_post = paginator.page(page)

    return render(request,"blog/index.html",{'page_obj': part_post})

def edit_post(request,post_id):
    posts = Post.objects.get(id=post_id)
    if request.method == 'POST':

        textarea = request.POST["body"]
        posts.post = textarea
        posts.save()
        return redirect("index")
    return render(request,"blog/edit.html",{
        "content":posts
    })

def delete(request,post_id):
    posts = Post.objects.get(id=post_id)
    posts.delete()
    return redirect("index")

def likes_up(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))


    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)

    return redirect('index')


def profile(request,username):
    my_account = get_object_or_404(User,username=username)
    my_post = Post.objects.filter(user=my_account).order_by("id")

    following = False

    if request.user.is_authenticated:
        followers = my_account.followers.filter(followed_by__id=request.user.id)
        following= True
        # if followers.exists():
        #     following = True



    return render(request,"blog/profile.html",{
        "posts":my_post,

        "post_count": my_post.count(),
    })


# def follow(request,username):
#     all_user = User.objects.all()
#     my_account = get_object_or_404(User,username=username)
#     my_post = Post.objects.filter(user=my_account).order_by("id")

#     following = False

#     if request.user.is_authenticated:
#         followers = my_account.followers.filter(followed_by_id=request.user.id)
#         # if followers.exists():
#         #     following = True


#     return render(request,"blog/following.html",{
#         "al_us": all_user,
#         "following":following
#     })


# def follow_or_unfollow_user(request,user_id):

#     followed = get_object_or_404(User,id=user_id)
#     followed_by = get_object_or_404(User,id=request.user.id)

#     follow,created =Follow.objects.get_or_create(followed_me=followed,followed_by=followed_by)

#     if created:
#         followed.followers.add(follow)

#     else:
#         followed.followers.remove(follow)
#         follow.delete()
#     return redirect('index')



# def follow_user(request, user_id):

#     following = User.objects.get(id=user_id)
#     Follow.objects.create(follower=request.user, following=following)
#     return redirect('index')

# def unfollow_user(request, user_id):
#     follower = request.user
#     following = User.objects.get(id=user_id)
#     Follow.objects.get(follower=follower, following=following).delete()
#     return redirect('index')

# def follow_user(request, user_id):
#     following_user = User.objects.get(id=user_id)
#     current_user = request.user
#     Follow.objects.create(follower=current_user, following=following_user).save()
#     return redirect('index')

# def unfollow_user(request, user_id):
#     following_user = User.objects.get(id=user_id)
#     current_user = request.user
#     Follow.objects.filter(follower=current_user, following=following_user)[0].delete()
#     return redirect('index')


