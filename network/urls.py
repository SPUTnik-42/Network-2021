
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("user-profile/<int:user_id>", views.user_profile, name="user-profile"),
    path("post/<str:action>", views.post, name="post"),
    path("following", views.following, name="following"),
    path("follow-unfollow/<int:user_id>", views.follow_unfollow, name="follow-unfollow"),
    path("like/<int:action_id>", views.like, name="like"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
