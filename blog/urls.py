from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("index/",views.index,name="index"),
    path("logout", views.logout_view, name="logout"),
    path('addpost/', views.addPost,name="addPosts"),
    path("edit-post/<int:post_id>", views.edit_post,name="edit-post"),
    path("delete/<int:post_id>", views.delete,name="delete"),
    path("like/",views.likes_up,name="like-post"),
    path("profile/<str:username>",views.profile,name="profile"),
    # path("follow/<str:username>",views.follow,name="follow"),
    # path("follow_or_unfollow/<int:user_id>",views.follow_or_unfollow_user,name="follow_or_unfollow")

]