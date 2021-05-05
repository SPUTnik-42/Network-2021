from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.paginator import Paginator
from .models import User, Post, Following, UserProfile, Like
from .forms import CreatePostForm
from django.contrib.auth.decorators import login_required
import json
from itertools import chain



def index(request):
    all_posts = Post.objects.order_by("-date").all()

    #Create page controll
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "post_form": CreatePostForm(),
        "page_obj": page_obj,
        "add_post_available": True
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url="network:login")
def user_profile(request, user_id):
    """ View: Shows requested user profile and the user's posts """

    user_data = User.objects.get(pk=user_id)
    posts = user_data.posts.order_by("-date").all()

    # Get following and followed user objects
    following_id_list = Following.objects.filter(user=user_id).values_list('user_followed', flat=True)
    followers_id_list = Following.objects.filter(user_followed=user_id).values_list('user_id', flat=True)

    following_user_list = User.objects.filter(id__in=following_id_list)
    followers_user_list = User.objects.filter(id__in=followers_id_list)

    # Create page controll
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/user_profile.html", {
        "user_data": user_data,
        "following": following_user_list,
        "followers": followers_user_list,
        "page_obj": page_obj,
    })


@login_required(login_url="network:login")
def follow_unfollow(request, user_id):
   
    # GET method is not allowed
    if request.method == "GET":
        return HttpResponse(status=405)
    # Nested try/except helps to reduce db queries by one
    if request.method == "POST":
        try:
            get_follow_obj = Following.objects.get(user=request.user.id, user_followed=user_id)
        except Following.DoesNotExist:
            try:
                user_to_follow = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return HttpResponse(status=404)
            else:
                new_follow_obj = Following(user=request.user, user_followed=user_to_follow)
                new_follow_obj.save()
        else:
            get_follow_obj.delete()

        return HttpResponseRedirect(reverse("user-profile", args=[user_id]))


@login_required(login_url="network:login")
def user_profile(request, user_id):
  

    user_data = User.objects.get(pk=user_id)
    posts = user_data.posts.order_by("-date").all()

    # Get following and followed user objects
    following_id_list = Following.objects.filter(user=user_id).values_list('user_followed', flat=True)
    followers_id_list = Following.objects.filter(user_followed=user_id).values_list('user_id', flat=True)

    following_user_list = User.objects.filter(id__in=following_id_list)
    followers_user_list = User.objects.filter(id__in=followers_id_list)

    # Create page controll
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/user_profile.html", {
        "user_data": user_data,
        "following": following_user_list,
        "followers": followers_user_list,
        "page_obj": page_obj
    })

@login_required(login_url="network:login")
def like(request,action_id):
    user = request.user
    if request.method == 'GET':
        #post_id = request.GET['post_id']
        likedpost = Post.objects.get(pk=action_id)
        if user in likedpost.liked.all():
            likedpost.liked.remove(user)
            like = Like.objects.get(post=likedpost, user=user)
            like.delete()
        else:
            like = Like.objects.get_or_create(post=likedpost, user=user)
            likedpost.liked.add(user)
            likedpost.save()
        
        return HttpResponse(status=204)

@login_required(login_url="network:login")
def following(request):
    """ View: Show users' posts that current user follows"""

    current_user = User.objects.get(pk=request.user.id)

    # Get all posts from users that current user follows
    posts = [users.get_user_followed_posts() for users in current_user.following.all()]

    # Flatten 2d array to 1d array
    posts = list(chain(*posts))

    # Create page controll
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "form": None,
        "page_obj": page_obj,
        "add_post_available": False
    })

def post(request, action):
    """ View: Controls saving a new post (only POST) """

    # Get not allowed
    if request.method == "GET":
        return HttpResponse(status=405)

    if request.method == "POST":
        if action == "post":
            form = CreatePostForm(request.POST)

            if form.is_valid():
                # Get all data from the form
                content = form.cleaned_data["content"]

                # Save the record
                post = Post(
                    user = User.objects.get(pk=request.user.id),
                    text = content
                )
                post.save()


        # Go back to the place from which the request came
        return HttpResponseRedirect(request.headers['Referer'])

    if request.method == "PUT":
        body = json.loads(request.body)
        # Query for requested post - make sure
        # that current user is the author
        try:
            if action == "post":
                object_to_edit = Post.objects.get(pk=body.get('id'), user=request.user)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return JsonResponse({
                "error": _("Post or Comment does not exist")
            }, status=404)

        # Update post's content
        object_to_edit.text = body.get('content')
        object_to_edit.save()

        # Return positive response
        return HttpResponse(status=201)

    if request.method == "DELETE":
        body = json.loads(request.body)
        # Query for requested post - make sure
        # that current user is the author
        try:
            if action == "post":
                object_to_delete = Post.objects.get(pk=body.get('id'), user=request.user)
        except (Post.DoesNotExist, Comment.DoesNotExist):
            return JsonResponse({
                "error": _("Post or Comment does not exist")
            }, status=404)

        # Delete the post and refresh the page
        object_to_delete.delete()
        return HttpResponse(status=204)