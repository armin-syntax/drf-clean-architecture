from django.urls import path

from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="user-list"),
    path("sync-users/", views.SyncUsersView.as_view(), name="sync-users"),
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("<str:username>/", views.UserProfileView.as_view(), name="user-profile"),
    path("<str:username>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("<str:username>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("<str:username>/follow/", views.UserFollowView.as_view(), name="user-follow"),
    path("<str:username>/unfollow/", views.UserUnfollowView.as_view(), name="user-unfollow"),
    path("<str:username>/followers/", views.UserFollowerListView.as_view(), name="user-followers"),
    path("<str:username>/following/", views.UserFollowingListView.as_view(), name="user-following"),
]
