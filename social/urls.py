from django.urls import path
from .views import PostListView,PostDetailView,EditPostView,DeletePostView,CommentDeleteView,UserProfileView,UpdateProfileView,ProfileSearch,AddLike,AddDisLike,AddFollower,RemoveFollower,FollowersList


urlpatterns = [
    path('',PostListView.as_view(),name="post_list"),
    path('post/<int:pk>/',PostDetailView.as_view(),name="post"),
    path('post/edit/<int:pk>/',EditPostView.as_view(),name="post-edit"),
    path('post/delete/<int:pk>/',DeletePostView.as_view(),name="post-delete"),
    path('post/<int:post_pk>/comment/delete/<int:pk>/',CommentDeleteView.as_view(),name="comment-delete"),
    path('profile/<int:pk>/',UserProfileView.as_view(),name="user-profile"),
    path('profile/edit/<int:pk>/',UpdateProfileView.as_view(),name="edit-profile"),
    path('search/',ProfileSearch.as_view(),name="search"),
    path('profile/<int:pk>/followers/',FollowersList.as_view(),name="followers-list"),
    path('post/<int:pk>/like',AddLike.as_view(),name="like"),
    path('post/<int:pk>/dislike',AddDisLike.as_view(),name="dislike"),
    path('profile/<int:pk>/follow/add',AddFollower.as_view(),name="follow"),
    path('profile/<int:pk>/follow/remove',RemoveFollower.as_view(),name="unfollow"),

]